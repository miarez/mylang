from typing import Callable, Dict
from llvmlite import ir

from src.compiler.utils.TypeCoercion import TypeCoercion


class BuiltinFunction:
    """Base class for all built-in function handlers."""
    def __init__(self, compiler) -> None:
        self.compiler = compiler

    def handle(self, args: list[ir.Value], types: list[ir.Type]) -> tuple[ir.Value, ir.Type]:
        """Override this in subclasses to handle the built-in function."""
        raise NotImplementedError("Built-in function handler must implement 'handle'.")

class BuiltinFunctionRegistry:
    """Registry for managing built-in functions."""
    def __init__(self) -> None:
        self.registry: Dict[str, Callable] = {}

    def register(self, name: str, handler_class: Callable) -> None:
        """Register a built-in function handler."""
        self.registry[name] = handler_class

    def get(self, name: str) -> Callable:
        """Retrieve the handler class for a built-in function."""
        return self.registry.get(name)


class PrintBuiltin(BuiltinFunction):
    """Handler for the 'print' built-in function."""
    def handle(self, args: list[ir.Value], types: list[ir.Type]) -> tuple[ir.Value, ir.Type]:
        if len(args) != 1:
            raise ValueError("print() expects exactly one argument.")

        value = args[0]
        value_type = types[0]

        # Coerce the value to a string if necessary
        if value_type != self.compiler.type_map["str"]:
            coercion_helper = TypeCoercion(self.compiler)
            value = coercion_helper.coerce_to_str(value, value_type)

        # Declare or retrieve the 'puts' function
        if "puts" not in self.compiler.module.globals:
            voidptr_ty = ir.IntType(8).as_pointer()  # i8*
            puts_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=False)
            puts_fn = ir.Function(self.compiler.module, puts_ty, name="puts")
        else:
            puts_fn = self.compiler.module.globals["puts"]

        # Call 'puts' with the coerced string
        self.compiler.builder.call(puts_fn, [value])

        # Return void (no meaningful return value for 'print')
        return None, ir.VoidType()

