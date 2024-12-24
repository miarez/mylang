from enum import Enum 

class NodeType(Enum):
    Program = "Program" # top most level 

    # Statements
    ExpressionStatement = "ExpressionStatement"
    LetStatement = "LetStatement"
    FunctionStatement = "FunctionStatement"
    BlockStatement = "BlockStatement"
    ReturnStatement = "ReturnStatement"
    AssignStatement = "AssignStatement"
    IfStatement = "IfStatement"


    # Expressions
    InfixExpression = "InfixExpression"
    CallExpression = "CallExpression"

    # Literals
    IntegerLiteral = "IntegerLiteral"
    FloatLiteral = "FloatLiteral"
    StringLiteral = "StringLiteral"
    IdentifierLiteral = "IdentifierLiteral"
    BooleanLiteral = "BooleanLiteral"

    # Helper
    FunctionParameter = "FunctionParameter"
