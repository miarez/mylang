from src.ast.statement.Statement import Statement
from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType


class AssignStatement(Statement):
    def __init__(self, identifier: Expression = None, right_value: Expression = None) -> None:
        self.identifier = identifier
        self.right_value = right_value

    def type(self) -> NodeType:
        return NodeType.AssignStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "identifier": self.identifier.json(),
            "right_value": self.right_value.json(),
        }
