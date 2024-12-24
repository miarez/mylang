from src.ast.statement.Statement import Statement
from src.ast.NodeType import NodeType

# This is like a Util tbh..
class FunctionParameter(Statement):
    def __init__(self, name:str, value_type:str = None) -> None:
        self.name = name 
        self.value_type = value_type

    def type(self) -> NodeType:
        return NodeType.FunctionParameter

    def json(self) -> dict:
        return {
            "type" : self.type().value,
            "name" : self.name,
            "value_type" : self.value_type            
        }
