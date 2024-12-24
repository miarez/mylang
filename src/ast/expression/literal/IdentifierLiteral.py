from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType

class IdentifierLiteral(Expression):
    def __init__(self, value: str = None) -> None:
        self.value = value
        super().__init__()

    def type(self) -> NodeType:
        return NodeType.IdentifierLiteral
    
    def json(self) -> dict:
        return {
            "type" : self.type().value, 
            "value" : self.value       
        }
