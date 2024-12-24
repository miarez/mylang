from typing import Any 
from dataclasses import dataclass

from src.lexer.TokenType import TokenType

@dataclass
class Token:
    def __init__(self, type : TokenType, literal: Any, line_no: int, position: int) -> None:
        self.type = type
        self.literal = literal 
        self.line_no = line_no
        self.position = position

    def __str__(self):
        return f"Token[{self.type} : {self.literal} : Line {self.line_no} : Position : {self.position}]"

    def __repr__(self) -> str:
        return str(self)


KEYWORDS: dict[str, TokenType] = {
    "let"   : TokenType.LET,
    "fn"    : TokenType.FN,
    "return": TokenType.RETURN,
    "if"    : TokenType.IF, 
    "else"    : TokenType.ELSE,     
    "true"    : TokenType.TRUE, 
    "false"    : TokenType.FALSE,         
}

TYPE_KEYWORDS: list[str] = [
    "str",
    "int",
    "float"
]

def lookup_identifier(identifier:str) -> TokenType:
    tokenType: TokenType | None = KEYWORDS.get(identifier)
    if tokenType is not None:
        return tokenType
    
    if identifier in TYPE_KEYWORDS:
        return TokenType.TYPE

    return TokenType.IDENTIFIER