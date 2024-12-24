from typing import Any 

from src.lexer.Token import Token, lookup_identifier
from src.lexer.TokenType import TokenType

class Lexer:
    def __init__(self, source : str) -> None:
        self.source = source

        self.position: int = -1
        self.read_position: int = 0
        self.line_no: int = 1

        self.current_char: str | None = None 

        self.__read_char()


    def __read_char(self) -> None:

        # are we at the end of the source code?
        if self.read_position >= len(self.source):
            self.current_char = None
        else: 
            self.current_char = self.source[self.read_position]
        
        self.position = self.read_position
        self.read_position += 1

    def __peek_char(self) -> str | None:
        if self.read_position >= len(self.source):
           return None
        
        return self.source[self.read_position]


    def __skip_whitespace(self) -> None :
        while self.current_char in [' ', '\t', '\n', '\r']:
            if(self.current_char == "\n"):
                self.line_no += 1
            
            self.__read_char()

    def __new_token(self, tokenType: TokenType, literal: Any) -> Token:
        return Token(type=tokenType, literal=literal, line_no=self.line_no, position=self.position)


    def __is_digit(self, character: str) -> bool:
        return '0' <= character and character <= '9'

    def __is_letter(self, character: str) -> bool:
        return 'a' <= character and character <= 'z' or 'A' <= character and character <= 'Z' or character == "_"



    def __read_number(self) -> Token:
        start_pos: int = self.position
        dot_count: int = 0 # (tracks how many decimals exists)

        output: str = ""
        while self.__is_digit(self.current_char) or self.current_char == ".":
            if(self.current_char == "."):
                dot_count += 1
            
            if dot_count > 1:
                print(f"Too many decimals in number on line {self.line_no} in position {self.position}")
                return self.__new_token(TokenType.ILLEGAL, self.source[start_pos:self.position])

            output += self.source[self.position]
            self.__read_char()

            if(self.current_char is None):
                break

        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))            



    def __read_identifier(self) -> str:
        position = self.position
        while self.current_char is not None and (self.__is_letter(self.current_char) or self.current_char.isalnum()):
            self.__read_char()

        return self.source[position:self.position]

    def next_token(self) -> Token:
        token: Token = None 
        self.__skip_whitespace()

        match self.current_char:

            case '"':
                literal_str = self.__read_string()
                return self.__new_token(TokenType.STR, literal_str)
            case "+":
                token = self.__new_token(TokenType.PLUS, self.current_char)
            case "-":
                # handle -> arrow
                if self.__peek_char() == ">":
                    character: str = self.current_char
                    self.__read_char()
                    token = self.__new_token(TokenType.ARROW, character + self.current_char)                    
                else:
                    token = self.__new_token(TokenType.MINUS, self.current_char)                    
            case "*":
                token = self.__new_token(TokenType.MULTIPLY, self.current_char)
            case "/":
                token = self.__new_token(TokenType.DIVIDE, self.current_char)
            case "^":
                token = self.__new_token(TokenType.POW, self.current_char)
            case "%":
                token = self.__new_token(TokenType.MODULUS, self.current_char)

            case "<":
                if self.__peek_char() == "=":
                    character = self.current_char
                    self.__read_char()
                    token = self.__new_token(TokenType.LT_EQ, character + self.current_char)
                else:
                    token = self.__new_token(TokenType.LT, self.current_char)

            case ">":
                if self.__peek_char() == "=":
                    character = self.current_char
                    self.__read_char()
                    token = self.__new_token(TokenType.GT_EQ, character + self.current_char)
                else:
                    token = self.__new_token(TokenType.GT, self.current_char)

            case "=":
                if self.__peek_char() == "=":
                    character = self.current_char
                    self.__read_char()
                    token = self.__new_token(TokenType.EQ_EQ, character + self.current_char)
                else:
                    token = self.__new_token(TokenType.EQ, self.current_char)

            case "!":
                if self.__peek_char() == "=":
                    character = self.current_char
                    self.__read_char()
                    token = self.__new_token(TokenType.NOT_EQ, character + self.current_char)
                else:
                    token = self.__new_token(TokenType.ILLEGAL, self.current_char)


            case ";":
                token = self.__new_token(TokenType.SEMICOLON, self.current_char)
            case "(":
                token = self.__new_token(TokenType.LPAREN, self.current_char)
            case ")":
                token = self.__new_token(TokenType.RPAREN, self.current_char)

            case "{":
                token = self.__new_token(TokenType.LBRACE, self.current_char)
            case "}":
                token = self.__new_token(TokenType.RBRACE, self.current_char)


            case ":":
                token = self.__new_token(TokenType.COLON, self.current_char)

            case ",":
                token = self.__new_token(TokenType.COMMA, self.current_char)

            case None:
                token = self.__new_token(TokenType.EOF, "")                



            # default in python for match
            case _:
                if self.__is_letter(self.current_char):
                    literal: str = self.__read_identifier()
                    tokenType:TokenType = lookup_identifier(literal)
                    token: Token = self.__new_token(tokenType=tokenType, literal=literal)
                    return token
                
                elif self.__is_digit(self.current_char):
                    token = self.__read_number()
                    return token
                else:
                    token = self.__new_token(TokenType.ILLEGAL, self.current_char)

        self.__read_char()
        return token
    
    def __read_string(self) -> str:
        # Skip the opening quote
        self.__read_char()
        start_position = self.position

        # Read until the next quote or EOF
        s = []
        while self.current_char is not None and self.current_char != '"':
            s.append(self.current_char)
            self.__read_char()

        # self.current_char == '"' means we found the end-of-string
        # or None means EOF

        # Skip the closing quote if present
        if self.current_char == '"':
            self.__read_char()

        return "".join(s)

