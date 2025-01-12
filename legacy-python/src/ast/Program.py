from typing import List

from src.ast.Node import Node 
from src.ast.NodeType import NodeType
from src.ast.statement.Statement import Statement


class Program(Node):
    def __init__(self) -> None:
        super().__init__()
        self.statements: List[Statement] = [] 

    def type(self) -> NodeType:
        return NodeType.Program 
    

    def json(self) -> dict:
        return {
            "type" : self.type().value,
            # recursively build out json AST file
            "statements" : [{statement.type().value: statement.json()} for statement in self.statements]
        }
