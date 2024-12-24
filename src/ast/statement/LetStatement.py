from src.ast.statement.Statement import Statement
from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType

class LetStatement(Statement):
    def __init__(self, name:Expression = None, value:Expression = None, value_type:str = None) -> None:
        self.name = name
        self.value = value
        self.value_type = value_type

    def type(self) -> NodeType:
        return NodeType.LetStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.json(),
            "value": self.value.json(),
            "value_type": self.value_type
        }