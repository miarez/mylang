from src.ast.statement.Statement import Statement
from src.ast.NodeType import NodeType
from src.ast.expression.Expression import Expression

class ExpressionStatement(Statement):
    def __init__(self, expression:Expression = None) -> None:
        self.expression = expression
        super().__init__()

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement

    def json(self) -> dict:
        return {
            "type" : self.type().value,
            "expression" : self.expression.json()
        }
