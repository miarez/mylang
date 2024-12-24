from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType


class CallExpression(Expression):
    def __init__(self, function: Expression = None, arguments: list[Expression] = None) -> None:
        self.function = function
        self.arguments = arguments

    def type(self) -> NodeType:
        return NodeType.CallExpression
    
    def json(self) -> dict:
        return {
            "type" : self.type().value, 
            "function" : self.function.json(),
            "arguments" : [arg.json() for arg in self.arguments]
        }