from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType
    
class StringLiteral(Expression):
    def __init__(self, value: str = None) -> None:
        super().__init__()
        self.value = value

    def type(self) -> NodeType:
        return NodeType.StringLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }    
