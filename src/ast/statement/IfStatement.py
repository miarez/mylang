from src.ast.statement.Statement import Statement
from src.ast.NodeType import NodeType
from src.ast.expression.Expression import Expression
from src.ast.statement.BlockStatement import BlockStatement


class IfStatement(Statement):
    def __init__(self, 
                 condition:Expression = None,
                 consenquence: BlockStatement = None,
                 alternative: BlockStatement = None
                 ) -> None:
        self.condition = condition
        self.consenquence = consenquence
        self.alternative = alternative


    def type(self) -> NodeType:
        return NodeType.IfStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "condition": self.condition.json(),
            "consenquence": self.consenquence.json(),
            "alternative": self.alternative.json() if self.alternative is not None else None
        }
        