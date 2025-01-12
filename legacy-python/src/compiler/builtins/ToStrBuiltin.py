# src/compiler/builtins/to_str.py

from llvmlite import ir

class ToStrBuiltin:
    """
    Implements the built-in function `to_str`, which converts supported types
    (e.g., integers and arrays of integers) into their string representations.

    Example outputs:
    - int:    123   -> "123"
    - array: [1, 2] -> "[1, 2]"
    
    This works at a very low level by interacting with LLVM IR to:
    - Allocate memory for strings on the stack.
    - Convert values to strings using external functions like `sprintf`.
    - Build up strings character by character or component by component.
    """

    def __init__(self, compiler):
        # The compiler instance gives us access to the IR builder, module, and type mappings.
        self.compiler = compiler
        self.builder = compiler.builder
        self.module = compiler.module

    def handle(self, args, types):
        """
        Main entry point for the `to_str` built-in.
        This method determines the type of the argument and dispatches
        to the appropriate conversion logic.

        Arguments:
        - args: A list of ir.Value objects (LLVM IR values passed as arguments).
        - types: A list of ir.Type objects (corresponding LLVM IR types).

        Returns:
        - A tuple (result_value, result_type), where:
          - result_value is an LLVM pointer to the string representation.
          - result_type is `i8*` (a C-style string).
        """
        if len(args) != 1:
            raise ValueError("to_str() expects exactly one argument.")

        # Extract the argument and its type
        arg, arg_type = args[0], types[0]

        # If it's an integer (i32), convert it to a string
        if arg_type == self.compiler.type_map["int"]:
            return self.int_to_str(arg)

        # If it's a pointer to an array (e.g., [N x i32]*), convert it to a string
        if isinstance(arg_type, ir.PointerType) and isinstance(arg_type.pointee, ir.ArrayType):
            return self.array_to_str(arg, arg_type.pointee)

        # If we don't support this type, raise an error
        raise TypeError(f"to_str does not support type '{arg_type}' yet.")

    # ----------------------------------------------------------------------
    # int -> string: e.g. "123"
    # ----------------------------------------------------------------------
    def int_to_str(self, int_val: ir.Value):
        """
        Converts a 32-bit integer (`i32`) into its string representation.

        Process:
        - Allocates ~12 bytes of memory on the stack for the result string.
        - Calls `sprintf` to format the integer as a string.

        Arguments:
        - int_val: The LLVM IR value representing the integer.

        Returns:
        - (i8*, i8* type): A pointer to the resulting string and its type.
        """
        builder = self.builder

        # Allocate a buffer on the stack for the string (12 bytes is enough for an int)
        buf_size = 12  # Covers largest 32-bit integer: "-2147483648" + null terminator
        buf_type = ir.ArrayType(ir.IntType(8), buf_size)  # [12 x i8]
        buf_ptr = builder.alloca(buf_type, name="inttmp")  # Allocate memory

        # Convert [12 x i8]* into i8* (pointer to the start of the buffer)
        zero_64 = ir.Constant(ir.IntType(64), 0)
        buf_i8ptr = builder.gep(buf_ptr, [zero_64, zero_64], name="buf_i8ptr")

        # Create a global format string "%d" (used by sprintf to format integers)
        fmt_int = self.get_global_string("%d")

        # Call sprintf(buf, "%d", int_val) to write the integer into the buffer
        sprintf_fn = self.get_or_declare_sprintf()
        builder.call(sprintf_fn, [buf_i8ptr, fmt_int, int_val])

        # Return the buffer pointer (i8*) and the type (i8*)
        return buf_i8ptr, self.compiler.type_map["str"]

    # ----------------------------------------------------------------------
    # array -> string: e.g. "[1, 2, 3]"
    # ----------------------------------------------------------------------
    def array_to_str(self, arr_ptr: ir.Value, arr_type: ir.types.ArrayType):
        """
        Converts an array pointer (e.g., [N x i32]*) into a string representation.

        Process:
        - Allocates a large buffer (256 bytes) for the resulting string.
        - Writes the opening "[" to the buffer.
        - Loops over each element in the array:
          - Converts each element to a string using `int_to_str`.
          - Appends the string to the buffer, adding ", " between elements.
        - Writes the closing "]" to the buffer.

        Arguments:
        - arr_ptr: The LLVM pointer to the array.
        - arr_type: The LLVM type of the array (e.g., [N x i32]).

        Returns:
        - (i8*, i8* type): A pointer to the resulting string and its type.
        """
        builder = self.builder
        element_count = arr_type.count  # Number of elements in the array
        element_type = arr_type.element  # Type of each element (e.g., i32)

        # Allocate a large buffer for the resulting string on the stack
        buf_size = 256  # Fixed size buffer for simplicity
        buf_type = ir.ArrayType(ir.IntType(8), buf_size)  # [256 x i8]
        buf_ptr = builder.alloca(buf_type, name="arrtmp")  # [256 x i8]*

        # Allocate an `i64` offset to track where in the buffer we're writing
        offset_ptr = builder.alloca(ir.IntType(64), name="offset")  # i64*
        builder.store(ir.Constant(ir.IntType(64), 0), offset_ptr)  # Initialize offset to 0

        # Convert [256 x i8]* into i8* (pointer to the start of the buffer)
        zero_64 = ir.Constant(ir.IntType(64), 0)
        buf_i8ptr = builder.gep(buf_ptr, [zero_64, zero_64], name="buf_i8ptr")

        # Write the opening "[" to the buffer
        self.append_string(buf_i8ptr, offset_ptr, "[")

        # Loop over each element in the array
        for i in range(element_count):
            idx_32 = ir.Constant(ir.IntType(32), i)  # Convert index to i32
            elem_ptr = builder.gep(arr_ptr, [zero_64, idx_32], name=f"elem_ptr_{i}")  # Get element pointer
            elem_val = builder.load(elem_ptr, name=f"elem_val_{i}")  # Load element value

            # If it's not the first element, append ", "
            if i > 0:
                self.append_string(buf_i8ptr, offset_ptr, ", ")

            # Convert the element to a string
            elem_str_ptr, _ = self.int_to_str(elem_val)

            # Append the element's string to the buffer
            self.append_cstring(buf_i8ptr, offset_ptr, elem_str_ptr)

        # Write the closing "]" to the buffer
        self.append_string(buf_i8ptr, offset_ptr, "]")

        # Return the buffer pointer (i8*) and its type
        return buf_i8ptr, self.compiler.type_map["str"]

    # ----------------------------------------------------------------------
    # Utility: append a literal string (like "[" or ", ") into the buffer
    # ----------------------------------------------------------------------
    def append_string(self, buf_i8ptr: ir.Value, offset_ptr: ir.Value, text: str):
        """
        Writes a Python string literal (e.g., "[", ", ", "]") to the buffer.

        Process:
        - Determines where to write using the current `offset`.
        - Calls sprintf(buf + offset, "%s", text).
        - Updates `offset` to reflect the number of bytes written.

        Arguments:
        - buf_i8ptr: Pointer to the start of the buffer.
        - offset_ptr: Pointer to the current offset in the buffer.
        - text: The Python string literal to append.
        """
        builder = self.builder

        # Convert the text into a global string (null-terminated)
        text_ptr = self.get_global_string(text)

        # Load the current offset
        old_offset = builder.load(offset_ptr, name="old_offset")

        # Calculate the destination pointer (buf + offset)
        dest_ptr = builder.gep(buf_i8ptr, [old_offset], name="dest_ptr")

        # Call sprintf(dest, "%s", text)
        sprintf_fn = self.get_or_declare_sprintf()
        fmt_s = self.get_global_string("%s")
        builder.call(sprintf_fn, [dest_ptr, fmt_s, text_ptr])

        # Increment the offset by the length of the string
        text_len = len(text)  # Known at compile-time
        new_offset = builder.add(old_offset, ir.Constant(ir.IntType(64), text_len))
        builder.store(new_offset, offset_ptr)

    # ----------------------------------------------------------------------
    # Utility: append a C-string (null-terminated i8*) into the buffer
    # ----------------------------------------------------------------------
    def append_cstring(self, buf_i8ptr: ir.Value, offset_ptr: ir.Value, cstr_ptr: ir.Value):
        """
        Appends a C-style string (e.g., the output of `int_to_str`) to the buffer.

        Process:
        - Determines where to write using the current `offset`.
        - Calls sprintf(buf + offset, "%s", cstr_ptr).
        - Updates `offset` using strlen(cstr_ptr).

        Arguments:
        - buf_i8ptr: Pointer to the start of the buffer.
        - offset_ptr: Pointer to the current offset in the buffer.
        - cstr_ptr: Pointer to the null-terminated string to append.
        """
        builder = self.builder

        # Load the current offset
        old_offset = builder.load(offset_ptr, name="old_offset")

        # Calculate the destination pointer (buf + offset)
        dest_ptr = builder.gep(buf_i8ptr, [old_offset], name="dest_ptr")

        # Call sprintf(dest_ptr, "%s", cstr_ptr)
        sprintf_fn = self.get_or_declare_sprintf()
        fmt_s = self.get_global_string("%s")
        builder.call(sprintf_fn, [dest_ptr, fmt_s, cstr_ptr])

        # Determine the length of the string using strlen
        strlen_fn = self.declare_or_get_strlen()
        cstr_len = builder.call(strlen_fn, [cstr_ptr], name="cstr_len")

        # Increment the offset by the length of the string
        new_offset = builder.add(old_offset, cstr_len)
        builder.store(new_offset, offset_ptr)

    # ----------------------------------------------------------------------
    # Utility: declare sprintf (if not already declared)
    # ----------------------------------------------------------------------
    def get_or_declare_sprintf(self) -> ir.Function:
        """
        Declares or retrieves the external `sprintf` function:
        int sprintf(char* buffer, const char* format, ...).

        Returns:
        - The LLVM IR function object for `sprintf`.
        """
        try:
            return self.module.get_global("sprintf")
        except KeyError:
            # Declare sprintf: i32 sprintf(i8*, i8*, ...)
            sprintf_ty = ir.FunctionType(
                ir.IntType(32),
                [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()],
                var_arg=True
            )
            return ir.Function(self.module, sprintf_ty, name="sprintf")

    # ----------------------------------------------------------------------
    # Utility: declare strlen (if not already declared)
    # ----------------------------------------------------------------------
    def declare_or_get_strlen(self) -> ir.Function:
        """
        Declares or retrieves the external `strlen` function:
        size_t strlen(const char*).

        Returns:
        - The LLVM IR function object for `strlen`.
        """
        try:
            return self.module.get_global("strlen")
        except KeyError:
            strlen_ty = ir.FunctionType(
                ir.IntType(64), [ir.IntType(8).as_pointer()], var_arg=False
            )
            return ir.Function(self.module, strlen_ty, name="strlen")

    # ----------------------------------------------------------------------
    # Utility: store a Python string as a global constant
    # ----------------------------------------------------------------------
    def get_global_string(self, text: str) -> ir.Value:
        """
        Creates a global LLVM constant for a null-terminated string.

        Arguments:
        - text: The Python string to store.

        Returns:
        - An i8* pointer to the string in memory.
        """
        # Convert the text to bytes and append a null terminator
        data = bytearray(text.encode("utf8")) + b"\0"
        const_type = ir.ArrayType(ir.IntType(8), len(data))  # [N x i8]

        # Create a unique name for the string
        count = len(list(self.module.global_values))
        name = f".str_{count}"

        # Define the global variable
        global_var = ir.GlobalVariable(self.module, const_type, name=name)
        global_var.linkage = 'internal'
        global_var.global_constant = True
        global_var.initializer = ir.Constant(const_type, data)

        # Cast [N x i8]* -> i8* and return
        return global_var.bitcast(ir.IntType(8).as_pointer())
