from llvmlite import ir

class AddListsBuiltin:
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

        # Create a new list to store the result
        result_list_type = ir.ArrayType(element_type, list_size)
        result_list_ptr = self.compiler.builder.alloca(result_list_type, name="result_list")

        # Perform element-wise addition
        for i in range(list_size):
            idx = ir.Constant(ir.IntType(32), i)
            
            # Load elements from the input lists
            elem1_ptr = self.compiler.builder.gep(arg1, [ir.Constant(ir.IntType(32), 0), idx])
            elem2_ptr = self.compiler.builder.gep(arg2, [ir.Constant(ir.IntType(32), 0), idx])
            
            elem1 = self.compiler.builder.load(elem1_ptr)
            elem2 = self.compiler.builder.load(elem2_ptr)

            # Perform addition
            result_elem = self.compiler.builder.add(elem1, elem2)

            # Store the result element
            result_elem_ptr = self.compiler.builder.gep(result_list_ptr, [ir.Constant(ir.IntType(32), 0), idx])
            self.compiler.builder.store(result_elem, result_elem_ptr)

        return result_list_ptr, result_list_type
