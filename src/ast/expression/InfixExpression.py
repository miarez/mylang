from src.ast.expression.Expression import Expression
from src.ast.NodeType import NodeType

class InfixExpression(Expression):
    def __init__(self, left_node:Expression, operator: str, right_node:Expression) -> None:
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node        
        super().__init__()

    def type(self) -> NodeType:
        return NodeType.InfixExpression
    
    def json(self) -> dict:
        return {
            "type" : self.type().value, 
            "left_node" : self.left_node.json(),
            "operator" : self.operator,            
            "right_node" : self.right_node.json(),            
        }
