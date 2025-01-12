from llvmlite import ir

class AddListsBuiltin_vec:
    def __init__(self, compiler):
        self.compiler = compiler

    def handle(self, args, types):
        if len(args) != 2:
            raise ValueError("add_lists requires exactly two arguments.")
        
        # Validate that both arguments are lists of the same type
        arg1, arg2 = args
        type1, type2 = types

        if not isinstance(type1, ir.ArrayType) or not isinstance(type2, ir.ArrayType):
            raise ValueError("add_lists arguments must be lists.")
        
        if type1.element != type2.element or type1.count != type2.count:
            raise ValueError("add_lists requires lists of the same type and size.")
        
        element_type = type1.element
        list_size = type1.count

        # Define the vector type for SIMD operations
        vector_type = ir.VectorType(element_type, list_size)

        # Load the two input lists into vector registers
        vec1 = self.compiler.builder.load(self.compiler.builder.bitcast(arg1, vector_type.as_pointer()))
        vec2 = self.compiler.builder.load(self.compiler.builder.bitcast(arg2, vector_type.as_pointer()))

        # Perform SIMD addition
        result_vector = self.compiler.builder.add(vec1, vec2)

        # Store the result back into a new list
        result_list_type = ir.ArrayType(element_type, list_size)
        result_list_ptr = self.compiler.builder.alloca(result_list_type, name="result_list")

        self.compiler.builder.store(
            self.compiler.builder.bitcast(result_vector, result_list_ptr.type.as_pointer()),
            result_list_ptr
        )

        return result_list_ptr, result_list_type
