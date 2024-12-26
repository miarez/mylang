from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------
#  Environment
# --------------------------------------------------------------------
class Environment:
    """
    An environment holds variable bindings. Optionally, it can have
    a parent environment to allow for nested scopes (e.g. function calls).
    """
    def __init__(self, parent: 'Environment' = None):
        self.store: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        if name in self.store:
            return self.store[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' is not defined.")

    def set(self, name: str, value: Any) -> Any:
        self.store[name] = value
        return value

# --------------------------------------------------------------------
#  Special Classes for Return and Function
# --------------------------------------------------------------------
class ReturnValue(Exception):
    """
    Raised when a return statement is encountered in a function.
    """
    def __init__(self, value: Any):
        self.value = value

class FunctionObject:
    """
    Represents a user-defined function.
    """
    def __init__(self, name, parameters, body, return_type, defining_env):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type
        self.defining_env = defining_env

# --------------------------------------------------------------------
#  Interpreter
# --------------------------------------------------------------------
class Interpreter:
    """
    A tree-walking interpreter that executes the statements
    and expressions in the AST.
    """
    def __init__(self):
        self.global_env = Environment()
        self.builtin_functions = {
            "print": self.builtin_print
        }

    def interpret(self, program):
        """
        Interprets the provided program, starting from the top-level statements.
        If a 'main' function exists, it invokes it.
        """
        # Execute all top-level statements
        for stmt in program.statements:
            self.visit(stmt, self.global_env)

        # Check for and invoke the 'main' function
        if "main" in self.global_env.store:
            main_func = self.global_env.get("main")
            if isinstance(main_func, FunctionObject):
                return self.call_function(main_func, [])
            else:
                raise Exception("'main' is not callable.")
        else:
            raise Exception("No 'main' function defined.")

    # ----------------------------------------------------------------
    #  Built-in Functions
    # ----------------------------------------------------------------
    def builtin_print(self, *args):
        print(*args)
        return None

    # ----------------------------------------------------------------
    #  Node Visitors
    # ----------------------------------------------------------------
    def visit(self, node, env: Environment):
        """
        Dispatch method. Calls the appropriate visit method for the given node type.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, env)

    def no_visit_method(self, node, env):
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    def visit_Program(self, node, env: Environment):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt, env)
        return result

    # ----------------------------------------------------------------
    #  Statement Visitors
    # ----------------------------------------------------------------
    def visit_ExpressionStatement(self, node, env: Environment):
        return self.visit(node.expression, env)

    def visit_LetStatement(self, node, env: Environment):
        value = self.visit(node.value, env)
        env.set(node.name.value, value)
        return value

    def visit_AssignStatement(self, node, env: Environment):
        value = self.visit(node.right_value, env)
        env.set(node.identifier.value, value)
        return value

    def visit_ReturnStatement(self, node, env: Environment):
        value = self.visit(node.return_value, env)
        raise ReturnValue(value)

    def visit_BlockStatement(self, node, env: Environment):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt, env)
        return result

    def visit_IfStatement(self, node, env: Environment):
        condition = self.visit(node.condition, env)
        if self.is_truthy(condition):
            return self.visit(node.consenquence, env)
        elif node.alternative is not None:
            return self.visit(node.alternative, env)
        return None

    def visit_FunctionStatement(self, node, env: Environment):
        func_obj = FunctionObject(
            name=node.name.value,
            parameters=node.parameters,
            body=node.body,
            return_type=node.return_type,
            defining_env=env
        )
        env.set(node.name.value, func_obj)
        return func_obj

    # ----------------------------------------------------------------
    #  Expression Visitors
    # ----------------------------------------------------------------
    def visit_InfixExpression(self, node, env: Environment):
        left = self.visit(node.left_node, env)
        right = self.visit(node.right_node, env)
        op = node.operator

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        else:
            raise Exception(f"Unsupported operator: {op}")

    def visit_CallExpression(self, node, env: Environment):
        func = self.visit(node.function, env)
        args = [self.visit(arg, env) for arg in node.arguments]

        # Check if the function is a built-in
        if isinstance(func, str) and func in self.builtin_functions:
            return self.builtin_functions[func](*args)

        if isinstance(func, FunctionObject):
            return self.call_function(func, args)

        raise Exception(f"Not a callable object: {func}")

    def visit_IdentifierLiteral(self, node, env: Environment):
        if node.value in self.builtin_functions:
            return node.value
        return env.get(node.value)

    def visit_IntegerLiteral(self, node, env: Environment):
        return node.value

    def visit_FloatLiteral(self, node, env: Environment):
        return node.value

    def visit_StringLiteral(self, node, env: Environment):
        return node.value

    def visit_ListLiteral(self, node, env: Environment):
        return [self.visit(element, env) for element in node.elements]

    # ----------------------------------------------------------------
    #  Function Execution
    # ----------------------------------------------------------------
    def call_function(self, func_obj: FunctionObject, args: List[Any]):
        new_env = Environment(parent=func_obj.defining_env)

        if len(args) != len(func_obj.parameters):
            raise Exception(f"Function '{func_obj.name}' expected {len(func_obj.parameters)} arguments but got {len(args)}.")

        for param, arg in zip(func_obj.parameters, args):
            new_env.set(param.name, arg)

        try:
            self.visit(func_obj.body, new_env)
            return None  # Default return value if no return statement
        except ReturnValue as rv:
            return rv.value

    # ----------------------------------------------------------------
    #  Helpers
    # ----------------------------------------------------------------
    def is_truthy(self, value: Any) -> bool:
        return bool(value)
