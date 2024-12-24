from enum import Enum


class TokenType(Enum):
    # Special Tokens 
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"

    # Data Types
    INT = "INT"
    FLOAT = "FLOAT"
    IDENTIFIER = "IDENTIFIER" # the actual variable names
    STR = "STR"

    # ARITHMETIC SYMBOLS
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POW = "POW"
    MODULUS = "MODULUS"

    # ASSIGNMENT
    EQ = "EQ"

    # COMPARISON
    # Dont like that it breaks format here for some reason
    LT = "<"
    GT = ">"
    EQ_EQ = "=="
    NOT_EQ = "!="
    LT_EQ = "<="
    GT_EQ = ">="

    # SYMBOLS
    COLON = "COLON" 
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON" # END OF STATEMENT 
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    # SYMBOLS:FUNCTION DECLRATION
    ARROW = "ARROW" # FOR RETURN TYPE
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    # KEYWORDS
    LET = "LET"
    FN = "FN"
    RETURN = "RETURN"

    IF = "IF"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # Typing 
    TYPE = "TYPE"