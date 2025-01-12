from src.ast.statement.Statement import Statement
from src.ast.NodeType import NodeType

class BlockStatement(Statement):
    def __init__(self, statements: list[Statement] = None) -> None:
        self.statements = statements if statements is not None else []

    def type(self) -> NodeType:
        return NodeType.BlockStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [statement.json() for statement in self.statements]
        }
