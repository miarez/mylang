from llvmlite import ir

from src.ast.Node import Node 
from src.ast.NodeType import NodeType


from src.ast.Program import Program
from src.ast.statement.Statement import Statement 
from src.ast.statement.ExpressionStatement import ExpressionStatement
from src.ast.statement.LetStatement import LetStatement
from src.ast.statement.FunctionStatement import FunctionStatement
from src.ast.statement.ReturnStatement import ReturnStatement
from src.ast.statement.BlockStatement import BlockStatement
from src.ast.statement.AssignmentStatement import AssignStatement
from src.ast.statement.IfStatement import IfStatement

from src.ast.statement.FunctionParameter import FunctionParameter
from src.ast.expression.CallExpression import CallExpression
from src.ast.expression.InfixExpression import InfixExpression
from src.ast.expression.Expression import Expression
from src.ast.expression.literal.IntegerLiteral import IntegerLiteral
from src.ast.expression.literal.FloatLiteral import FloatLiteral
from src.ast.expression.literal.IdentifierLiteral import IdentifierLiteral
from src.ast.expression.literal.BooleanLiteral import BooleanLiteral
from src.ast.expression.literal.StringLiteral import StringLiteral

from src.compiler.Environment import Environment
from src.compiler.BuiltinFunctionRegistry import BuiltinFunctionRegistry, PrintBuiltin

class Compiler:
    def __init__(self) -> None:
        self.type_map: dict[str, ir.Type] = {
            "int" : ir.IntType(32),
            "float" : ir.FloatType(),
            "bool": ir.IntType(1),
            "str" : ir.IntType(8).as_pointer()
        }

        self.module:ir.Module = ir.Module("main")
        self.builder:ir.IRBuilder = ir.IRBuilder()
        self.environment = Environment()
        self.errors: list[str] = []
        self.builtin_registry = BuiltinFunctionRegistry()

        self.__initialize_builtins()



        

    def __initialize_builtins(self) -> None:

        self.builtin_registry.register("print", PrintBuiltin)

        def __init_booleans()-> tuple[ir.GlobalVariable, ir.GlobalVariable]:
            bool_type: ir.Type = self.type_map["bool"]

            true_var = ir.GlobalVariable(self.module, bool_type, 'true')
            true_var.initializer = ir.Constant(bool_type, 1)
            true_var.global_constant = True

            false_var = ir.GlobalVariable(self.module, bool_type, 'false')
            false_var.initializer = ir.Constant(bool_type, 0)
            false_var.global_constant = True

            return true_var, false_var

        true_var, false_var = __init_booleans()
        self.environment.define('true', true_var, true_var.type)
        self.environment.define('false', false_var, false_var.type)



    def compile(self, node:Node)->None:
        match node.type():
            case NodeType.Program:
                self.__visit_program(node)

            # Statement
            case NodeType.ExpressionStatement:
                self.__visit_expression_statement(node)
            case NodeType.LetStatement:
                self.__visit_let_statement(node)
            case NodeType.FunctionStatement:
                self.__visit_function_statement(node)
            case NodeType.BlockStatement:
                self.__visit_block_statement(node)
            case NodeType.ReturnStatement:
                self.__visit_return_statement(node)              
            case NodeType.AssignStatement:
                self.__visit_assignment_statement(node)
            case NodeType.IfStatement:
                self.__visit_if_statement(node)

            # Expressions
            case NodeType.InfixExpression:
                self.__visit_infix_expression(node)

            case NodeType.CallExpression:
                self.__visit_call_expression(node)


    # region Visit Methods (parent region)

    def __visit_program(self, node:Program) -> None:
        for statement in node.statements:
            self.compile(statement)


    # region Statements 

    def __visit_expression_statement(self, node:ExpressionStatement) -> None:
        self.compile(node.expression)

    def __visit_let_statement(self, node: LetStatement) -> None:
        name: str = node.name.value
        value: Expression = node.value 
        value_type: str = node.value_type # todo implement (once we are doing type checking)

        value, Type = self.__resolve_value(node=value)

        if self.environment.lookup(name) is None:
            # define and allocate the variable 
            pointer = self.builder.alloca(Type)

            # Store the value 
            self.builder.store(value, pointer)

            # Add the variable to the environment 
            self.environment.define(name, pointer, Type)
        else:
            pointer, _ = self.environment.lookup(name)
            self.builder.store(value, pointer)


    def __visit_block_statement(self, node: BlockStatement) -> None:
        for statement in node.statements:
            self.compile(statement)


    def __visit_return_statement(self, node:ReturnStatement) -> None:
        value: Expression = node.return_value
        value, Type = self.__resolve_value(value)
        self.builder.ret(value)

    def __visit_function_statement(self, node:FunctionStatement) -> None:
        name: str = node.name.value 
        body: BlockStatement = node.body 
        parameters: list[FunctionParameter] = node.parameters

        parameter_names: list[str] = [p.name for p in parameters]
        parameter_types: list[ir.Type] = [self.type_map[p.value_type] for p in parameters] 

        return_type: ir.Type = self.type_map[node.return_type]

        function_type: ir.FunctionType = ir.FunctionType(return_type, parameter_types)
        function: ir.Function = ir.Function(self.module, function_type, name=name)

        block: ir.Block = function.append_basic_block(f'{name}_entry')

        previous_builder = self.builder

        self.builder = ir.IRBuilder(block)

        # Storing Pointers To Each Parameter
        parameter_pointer_list = []
        for i, typ in enumerate(parameter_types):
            pointer = self.builder.alloca(typ=typ)
            self.builder.store(function.args[i], pointer)
            parameter_pointer_list.append(pointer)

        # Adding params to environment 
        previous_environment =self.environment
        self.environment = Environment(parent=self.environment)
        for i, x in enumerate(zip(parameter_types, parameter_names)):
            typ = parameter_types[i]
            pointer = parameter_pointer_list[i]

            self.environment.define(x[1], pointer, typ)

        self.environment.define(name, function, return_type)

        self.compile(body)

        # reset to previous scope
        self.environment = previous_environment

        # define again so global env has that function in scope 
        self.environment.define(name, function, return_type)

        # reset builder to previous builder 
        self.builder = previous_builder

    def __visit_assignment_statement(self, node: AssignStatement)-> None:
        name: str = node.identifier.value 
        value: Expression = node.right_value

        value, Type = self.__resolve_value(value)
        if self.environment.lookup(name) is None:
            self.errors.append(f"COMPILER ERROR: Identifier {name} has not been declared before it was re-assigned.")
        else:
            pointer, _  = self.environment.lookup(name)
            # store the new value to the existing pointer 
            self.builder.store(value, pointer)
        
    def __visit_if_statement(self, node:IfStatement) -> None:
        condition: Expression = node.condition
        consequence: BlockStatement = node.consenquence
        alternative: BlockStatement = node.alternative

        test, _ = self.__resolve_value(condition)

        if alternative is None:
            with self.builder.if_then(test):
                self.compile(consequence)
        else:
            with self.builder.if_else(test) as (true, otherwise):
                with true:
                    self.compile(consequence)

                with otherwise:
                    self.compile(alternative)



    # endregion

    # region Expressions 

    def __visit_infix_expression(self, node:InfixExpression) -> None:
        operator: str = node.operator
        left_value, left_type = self.__resolve_value(node.left_node)
        right_value, right_type = self.__resolve_value(node.right_node)

        value = None 
        Type = None
        
        # todo: float x int? 
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map["int"]
            match operator:
                case "+":
                    value = self.builder.add(left_value, right_value)
                case "-":
                    value = self.builder.sub(left_value, right_value)
                case "*":
                    value = self.builder.mul(left_value, right_value)
                case "/":
                    value = self.builder.sdiv(left_value, right_value)
                case "%":
                    value = self.builder.srem(left_value, right_value)
                case "^":
                    # todo
                    value = self.builder.sdiv(left_value, right_value)
                case "<":
                    value = self.builder.icmp_signed('<', left_value, right_value)
                    Type = ir.IntType(1)
                case "<=":
                    value = self.builder.icmp_signed('<=', left_value, right_value)
                    Type = ir.IntType(1)
                case ">":
                    value = self.builder.icmp_signed('>', left_value, right_value)
                    Type = ir.IntType(1)
                case ">=":
                    value = self.builder.icmp_signed('>=', left_value, right_value)
                    Type = ir.IntType(1)
                case "==":
                    value = self.builder.icmp_signed('==', left_value, right_value)
                    Type = ir.IntType(1)
                case "!=": 
                    value = self.builder.icmp_signed('!=', left_value, right_value)
                    Type = ir.IntType(1)

        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            Type = self.type_map["float"]
            match operator:
                case "+":
                    value = self.builder.fadd(left_value, right_value)
                case "-":
                    value = self.builder.fsub(left_value, right_value)
                case "*":
                    value = self.builder.fmul(left_value, right_value)
                case "/":
                    value = self.builder.fdiv(left_value, right_value)
                case "%":
                    value = self.builder.frem(left_value, right_value)
                case "^":
                    # todo
                    value = self.builder.sdiv(left_value, right_value)                                        
                case "<":
                    value = self.builder.fcmp_ordered('<', left_value, right_value)
                    Type = ir.IntType(1)
                case "<=":
                    value = self.builder.fcmp_ordered('<=', left_value, right_value)
                    Type = ir.IntType(1)
                case ">":
                    value = self.builder.fcmp_ordered('>', left_value, right_value)
                    Type = ir.IntType(1)
                case ">=":
                    value = self.builder.fcmp_ordered('>=', left_value, right_value)
                    Type = ir.IntType(1)
                case "==":
                    value = self.builder.fcmp_ordered('==', left_value, right_value)
                    Type = ir.IntType(1)
                case "!=": 
                    value = self.builder.fcmp_ordered('!=', left_value, right_value)
                    Type = ir.IntType(1)

        return value, Type
    

    def __visit_call_expression(self, node: CallExpression) -> tuple[ir.Value, ir.Type]:
        """
        Handles function calls, dynamically dispatching to built-in functions if needed,
        or to user-defined functions otherwise.
        """
        name: str = node.function.value  # The name of the function being called
        parameters: list[Expression] = node.arguments

        # Resolve arguments into LLVM IR values and their corresponding types
        args = []
        types = []

        for param in parameters:
            arg_val, arg_type = self.__resolve_value(param)
            args.append(arg_val)
            types.append(arg_type)

        # Check if this is a built-in function
        builtin_handler_class = self.builtin_registry.get(name)
        if builtin_handler_class:
            # Instantiate the handler and call 'handle'
            handler = builtin_handler_class(self)
            return handler.handle(args, types)

        # Otherwise, assume it's a user-defined function
        try:
            function, return_type = self.environment.lookup(name)
        except KeyError:
            raise ValueError(f"Function '{name}' not found in the current scope.")

        # Emit a call to the user-defined function
        ret = self.builder.call(function, args)
        return ret, return_type


    # endregion
        
    # endregion (parent region)


    # region Helper Methods

    def __resolve_value(self, node: Expression, value_type: str = None) -> tuple[ir.Value, ir.Type]:
        match node.type():
            case NodeType.IntegerLiteral:
                node:IntegerLiteral = node 
                value, Type = node.value, self.type_map["int"] if value_type is None else value_type
                return ir.Constant(Type, value), Type
            case NodeType.FloatLiteral:
                node:FloatLiteral = node 
                value, Type = node.value, self.type_map["float"] if value_type is None else value_type
                return ir.Constant(Type, value), Type
            case NodeType.IdentifierLiteral:
                node: IdentifierLiteral = node 
                pointer, Type = self.environment.lookup(node.value)
                return self.builder.load(pointer), Type
            case NodeType.BooleanLiteral:
                node: BooleanLiteral = node 
                return ir.Constant(ir.IntType(1), 1 if node.value else 0), ir.IntType(1)
            case NodeType.StringLiteral: 
                node: StringLiteral = node
                str_pointer = self.__create_string_constant(node.value)
                # type is i8* (i.e., "str")
                return str_pointer, self.type_map["str"]            

            case NodeType.InfixExpression:
                return self.__visit_infix_expression(node)

            case NodeType.CallExpression:
                return self.__visit_call_expression(node)
    # endregion

    def __create_string_constant(self, text: str) -> ir.Constant:
        byte_array = bytearray(text.encode("utf-8"))
        byte_array.append(0)

        str_type = ir.ArrayType(ir.IntType(8), len(byte_array))
        count = len(self.module.global_values)  # ALL global values, including functions
        name = f".str_{count}"

        global_var = ir.GlobalVariable(self.module, str_type, name=name)
        global_var.linkage = 'private'
        global_var.global_constant = True
        global_var.initializer = ir.Constant(str_type, byte_array)

        return global_var.bitcast(ir.IntType(8).as_pointer())