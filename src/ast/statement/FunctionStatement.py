from src.ast.statement.Statement import Statement
from src.ast.NodeType import NodeType
from src.ast.statement.FunctionParameter import FunctionParameter
from src.ast.statement.BlockStatement import BlockStatement

class FunctionStatement(Statement):
    def __init__(self, 
                 parameters: list[FunctionParameter] = [], 
                 body: BlockStatement = None, 
                 name = None, 
                 return_type:str = None) -> None:
        self.parameters = parameters
        self.body = body 
        self.name = name
        self.return_type = return_type

    def type(self) -> NodeType:
        return NodeType.FunctionStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.json(),
            "return_type": self.return_type,
            "parameters": [p.json() for p in self.parameters],
            "body": self.body.json()
        }