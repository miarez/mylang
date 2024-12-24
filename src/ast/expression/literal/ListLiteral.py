from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType


class ListLiteral(Expression):
    def __init__(self, elements: list[Expression]) -> None:
        self.elements = elements

    def type(self) -> NodeType:
        return NodeType.ListLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "elements": [element.json() for element in self.elements]
        }