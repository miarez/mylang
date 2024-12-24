from llvmlite import ir

class TypeCoercion:
    """Helper class to coerce LLVM types to string for printing."""
    def __init__(self, compiler):
        self.compiler = compiler

    def coerce_to_str(self, value: ir.Value, value_type: ir.Type) -> ir.Value:
        """
        Coerce an int, float, or bool LLVM value to a string representation.

        Args:
            value (ir.Value): The LLVM value to coerce.
            value_type (ir.Type): The LLVM type of the value.

        Returns:
            ir.Value: A pointer to the string representation of the value (i8*).
        """
        builder = self.compiler.builder
        module = self.compiler.module

        if value_type == self.compiler.type_map["int"]:
            return self.__int_to_str(value, builder, module)
        elif value_type == self.compiler.type_map["float"]:
            return self.__float_to_str(value, builder, module)
        elif value_type == self.compiler.type_map["bool"]:
            return self.__bool_to_str(value, builder, module)
        else:
            raise TypeError(f"Cannot coerce value of type {value_type} to string.")

    def __int_to_str(self, value: ir.Value, builder: ir.IRBuilder, module: ir.Module) -> ir.Value:
        """
        Convert an integer value to a string using sprintf.
        """
        # Create a format string for integers
        if "int_fmt" not in module.globals:
            fmt_type = ir.ArrayType(ir.IntType(8), 3)  # "%d\\0" has 3 characters
            int_fmt = ir.GlobalVariable(module, fmt_type, name="int_fmt")
            int_fmt.initializer = ir.Constant(fmt_type, bytearray("%d\0", "utf-8"))
            int_fmt.linkage = "private"
        else:
            int_fmt = module.globals["int_fmt"]

        # Cast the format string to i8* (char*)
        int_fmt_ptr = int_fmt.bitcast(ir.IntType(8).as_pointer())

        # Allocate space for the string
        str_buf = builder.alloca(ir.IntType(8), size=32, name="int_str_buf")

        # Call sprintf with the correct types
        sprintf_fn = self.__get_sprintf(module)
        builder.call(sprintf_fn, [str_buf, int_fmt_ptr, value])

        return str_buf


    def __float_to_str(self, value: ir.Value, builder: ir.IRBuilder, module: ir.Module) -> ir.Value:
        """
        Convert a float value to a string using sprintf.
        """
        # Create a format string for floats
        if "float_fmt" not in module.globals:
            fmt_type = ir.ArrayType(ir.IntType(8), 5)  # "%.2f\\0"
            float_fmt = ir.GlobalVariable(module, fmt_type, name="float_fmt")
            float_fmt.initializer = ir.Constant(fmt_type, bytearray("%.2f\0", "utf-8"))
            float_fmt.linkage = "private"
        else:
            float_fmt = module.globals["float_fmt"]

        # Cast the format string to i8* (char*)
        float_fmt_ptr = float_fmt.bitcast(ir.IntType(8).as_pointer())

        # Allocate space for the string
        str_buf = builder.alloca(ir.IntType(8), size=64, name="float_str_buf")

        # Convert float to double (LLVM IR `float` -> `double`)
        double_value = builder.fpext(value, ir.DoubleType())

        # Call sprintf with the correct types
        sprintf_fn = self.__get_sprintf(module)
        builder.call(sprintf_fn, [str_buf, float_fmt_ptr, double_value])

        return str_buf



    def __bool_to_str(self, value: ir.Value, builder: ir.IRBuilder, module: ir.Module) -> ir.Value:
        """
        Convert a boolean value to a string ("true" or "false").
        """
        true_str = self.compiler.__create_string_constant("true")
        false_str = self.compiler.__create_string_constant("false")
        return builder.select(value, true_str, false_str)

    def __get_sprintf(self, module: ir.Module) -> ir.Function:
        """
        Retrieve or declare the sprintf function.
        """
        if "sprintf" not in module.globals:
            sprintf_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()], var_arg=True)
            sprintf = ir.Function(module, sprintf_ty, name="sprintf")
        else:
            sprintf = module.globals["sprintf"]
        return sprintf
