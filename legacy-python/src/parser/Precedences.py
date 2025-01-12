from enum import Enum, auto 
from src.lexer.TokenType import TokenType 

# Precedence Types 
class PrecedenceType(Enum):

    # auto increments based on order of my code (allows to re-arrange stuff later)
    P_LOWEST: int = 0
    P_EQUALS = auto()
    P_LESSSGREATER = auto()
    P_SUM = auto()
    P_PRODUCT = auto()
    P_EXPONENT  = auto()
    P_PREFIX = auto()
    P_CALL = auto()
    P_INDEX = auto()

# Precedence Mapping 
PRECEDENCES: dict[TokenType, PrecedenceType] = {
    TokenType.PLUS : PrecedenceType.P_SUM,
    TokenType.MINUS : PrecedenceType.P_SUM,
    TokenType.DIVIDE : PrecedenceType.P_PRODUCT,
    TokenType.MULTIPLY : PrecedenceType.P_PRODUCT,
    TokenType.MODULUS : PrecedenceType.P_PRODUCT,
    TokenType.POW : PrecedenceType.P_EXPONENT,

    TokenType.EQ_EQ : PrecedenceType.P_EQUALS,
    TokenType.NOT_EQ : PrecedenceType.P_EQUALS,
    TokenType.LT : PrecedenceType.P_LESSSGREATER,
    TokenType.GT : PrecedenceType.P_LESSSGREATER,
    TokenType.LT_EQ : PrecedenceType.P_LESSSGREATER,
    TokenType.GT_EQ : PrecedenceType.P_LESSSGREATER,    

    TokenType.LPAREN : PrecedenceType.P_CALL,
}
