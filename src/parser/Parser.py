from typing import Callable 

from src.lexer.Lexer import Lexer 
from src.lexer.Token import Token, TokenType 
from src.parser.Precedences import PrecedenceType, PRECEDENCES

from src.ast.Program import Program
from src.ast.statement.Statement import Statement 
from src.ast.statement.ExpressionStatement import ExpressionStatement
from src.ast.statement.LetStatement import LetStatement
from src.ast.statement.FunctionStatement import FunctionStatement
from src.ast.statement.ReturnStatement import ReturnStatement
from src.ast.statement.BlockStatement import BlockStatement
from src.ast.statement.AssignmentStatement import AssignStatement
from src.ast.statement.IfStatement import IfStatement

from src.ast.statement.FunctionParameter import FunctionParameter
from src.ast.expression.CallExpression import CallExpression
from src.ast.expression.InfixExpression import InfixExpression
from src.ast.expression.Expression import Expression
from src.ast.expression.literal.IntegerLiteral import IntegerLiteral
from src.ast.expression.literal.FloatLiteral import FloatLiteral
from src.ast.expression.literal.IdentifierLiteral import IdentifierLiteral
from src.ast.expression.literal.BooleanLiteral import BooleanLiteral
from src.ast.expression.literal.StringLiteral import StringLiteral
from src.ast.expression.literal.ListLiteral import ListLiteral

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.errors: list[str] = []
        self.current_token: Token = None 
        self.peek_token: Token = None 

        self.prefix_parse_functions: dict[TokenType, Callable] = {
            TokenType.IDENTIFIER : self.__parse_identifier,
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_grouped_expression,
            TokenType.IF: self.__parse_if_statement,
            TokenType.TRUE: self.__parse_boolean,
            TokenType.FALSE: self.__parse_boolean,
            TokenType.STR: self.__parse_string_literal,            
            TokenType.LBRACKET: self.__parse_list_literal,            
            TokenType.LBRACE: self.__parse_block_statement  # Add support for blocks as expressions
        } 

        self.infix_parse_functions: dict[TokenType, Callable] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.DIVIDE: self.__parse_infix_expression,
            TokenType.MULTIPLY: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.MODULUS: self.__parse_infix_expression, 
            TokenType.EQ_EQ: self.__parse_infix_expression,
            TokenType.NOT_EQ: self.__parse_infix_expression,
            TokenType.LT: self.__parse_infix_expression,
            TokenType.GT: self.__parse_infix_expression,
            TokenType.LT_EQ: self.__parse_infix_expression,                                                
            TokenType.GT_EQ: self.__parse_infix_expression,
            TokenType.LPAREN: self.__parse_call_expression,
        }

        self.__next_token()
        self.__next_token()

    def __next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def __curent_token_is(self, tokenType: TokenType) -> bool:
        return self.current_token.type == tokenType        

    def __peek_token_is(self, tokenType: TokenType) -> bool:
        return self.peek_token.type == tokenType

    def __expect_peek(self, tokenType: TokenType) -> bool:
        if self.__peek_token_is(tokenType):
            self.__next_token()
            return True
        else:
            self.__peek_error(tokenType)
            return False

    def __current_precedence(self) -> PrecedenceType:
        precedence: int | None = PRECEDENCES.get(self.current_token.type)
        if precedence is None:
            return PrecedenceType.P_LOWEST
        return precedence
    
    def __peek_precedence(self) -> PrecedenceType:
        precedence: int | None = PRECEDENCES.get(self.peek_token.type)
        if precedence is None:
            return PrecedenceType.P_LOWEST
        return precedence
        
    def __peek_error(self, tokenType: TokenType) -> None:
        self.errors.append(f"Expected next token to be {tokenType}, got {self.peek_token.type} instead")

    def __no_prefix_parse_function_error(self, tokenType: TokenType) -> None:
        self.errors.append(f"No Prefix Parse Function for {tokenType} Found")

    def parse_program(self) -> Program:
        program: Program = Program()
        while self.current_token.type != TokenType.EOF:
            statement: Statement = self.__parse_statement()
            if statement is not None:
                program.statements.append(statement)
            self.__next_token()
        return program

    def __parse_statement(self) -> Statement:
        if self.current_token.type == TokenType.IDENTIFIER and self.__peek_token_is(TokenType.EQ):
            return self.__parse_assignment_statement()
        match self.current_token.type:
            case TokenType.LET:
                return self.__parse_let_statement()
            case TokenType.FN:
                return self.__parse_function_statement()
            case TokenType.RETURN:
                return self.__parse_return_statement()
            case TokenType.LBRACE:  # Handle block statements directly
                return self.__parse_block_statement()
            case _:
                return self.__parse_expression_statement()

    def __parse_expression_statement(self) -> ExpressionStatement:
        expression = self.__parse_expression(PrecedenceType.P_LOWEST)
        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()
        return ExpressionStatement(expression=expression)

    def __parse_let_statement(self) -> LetStatement:
        statement: LetStatement = LetStatement()
        if not self.__expect_peek(TokenType.IDENTIFIER):
            return None
        statement.name = IdentifierLiteral(value=self.current_token.literal)
        if not self.__expect_peek(TokenType.COLON):
            return None
        if not self.__expect_peek(TokenType.TYPE):
            return None
        statement.value_type = self.current_token.literal
        if not self.__expect_peek(TokenType.EQ):
            return None
        self.__next_token()
        statement.value = self.__parse_expression(PrecedenceType.P_LOWEST)
        while not self.__curent_token_is(TokenType.SEMICOLON) and not self.__curent_token_is(TokenType.EOF):
            self.__next_token()
        return statement

    def __parse_function_statement(self) -> FunctionStatement:
        statement: FunctionStatement = FunctionStatement()
        if not self.__expect_peek(TokenType.IDENTIFIER):
            return None
        statement.name = IdentifierLiteral(value=self.current_token.literal)
        if not self.__expect_peek(TokenType.LPAREN):
            return None
        statement.parameters = self.__parse_function_parameters()
        if not self.__expect_peek(TokenType.ARROW):
            return None
        if not self.__expect_peek(TokenType.TYPE):
            return None
        statement.return_type = self.current_token.literal
        if not self.__expect_peek(TokenType.LBRACE):
            return None
        statement.body = self.__parse_block_statement()
        return statement

    def __parse_function_parameters(self) -> list[FunctionParameter]:
        parameters: list[FunctionParameter] = []
        if self.__peek_token_is(TokenType.RPAREN):
            self.__next_token()
            return parameters
        self.__next_token()
        first_parameter: FunctionParameter = FunctionParameter(name=self.current_token.literal)
        if not self.__expect_peek(TokenType.COLON):
            return None
        self.__next_token()
        first_parameter.value_type = self.current_token.literal
        parameters.append(first_parameter)
        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()
            parameter: FunctionParameter = FunctionParameter(name=self.current_token.literal)
            if not self.__expect_peek(TokenType.COLON):
                return None
            self.__next_token()
            parameter.value_type = self.current_token.literal
            parameters.append(parameter)
        if not self.__expect_peek(TokenType.RPAREN):
            return None
        return parameters

    def __parse_return_statement(self) -> ReturnStatement:
        statement: ReturnStatement = ReturnStatement()
        self.__next_token()
        statement.return_value = self.__parse_expression(PrecedenceType.P_LOWEST)
        if not self.__expect_peek(TokenType.SEMICOLON):
            return None
        return statement

    def __parse_block_statement(self) -> BlockStatement:
        block_statement: BlockStatement = BlockStatement()
        self.__next_token()
        while not self.__curent_token_is(TokenType.RBRACE) and not self.__curent_token_is(TokenType.EOF):
            statement: Statement = self.__parse_statement()
            if statement is not None:
                block_statement.statements.append(statement)
            self.__next_token()
        return block_statement

    def __parse_assignment_statement(self) -> AssignStatement:
        statement: AssignStatement = AssignStatement()
        statement.identifier = IdentifierLiteral(value=self.current_token.literal)
        self.__next_token() # skips Identifier
        self.__next_token() # Skips EQ 
        statement.right_value = self.__parse_expression(PrecedenceType.P_LOWEST)
        self.__next_token()
        return statement

    def __parse_if_statement(self) -> IfStatement:
        condition: Expression = None
        consequence: BlockStatement = None
        alternative: BlockStatement = None
        self.__next_token()
        condition = self.__parse_expression(PrecedenceType.P_LOWEST)
        if not self.__expect_peek(TokenType.LBRACE):
            return None
        consequence = self.__parse_block_statement()
        if self.__peek_token_is(TokenType.ELSE):            
            self.__next_token()
            if not self.__expect_peek(TokenType.LBRACE):
                return None
            alternative = self.__parse_block_statement()
        return IfStatement(condition=condition, consenquence=consequence, alternative=alternative)

    def __parse_expression(self, precedence: PrecedenceType) -> Expression:
        prefix_function: Callable | None = self.prefix_parse_functions.get(self.current_token.type)
        if prefix_function is None:
            self.__no_prefix_parse_function_error(self.current_token.type)
            return None
        left_expression: Expression = prefix_function()
        while not self.__peek_token_is(TokenType.SEMICOLON) and precedence.value < self.__peek_precedence().value:
            infix_function: Callable | None = self.infix_parse_functions.get(self.peek_token.type)
            if infix_function is None:
                return left_expression
            self.__next_token()
            left_expression = infix_function(left_expression)
        return left_expression

    def __parse_infix_expression(self, left_node: Expression) -> Expression:
        infix_expression: InfixExpression = InfixExpression(left_node=left_node, operator=self.current_token.literal, right_node=None)
        precedence = self.__current_precedence()
        self.__next_token()
        infix_expression.right_node = self.__parse_expression(precedence)
        return infix_expression

    def __parse_grouped_expression(self) -> Expression:
        self.__next_token()
        expression: Expression = self.__parse_expression(PrecedenceType.P_LOWEST)
        if not self.__expect_peek(TokenType.RPAREN):
            return None
        return expression

    def __parse_call_expression(self, function: Expression) -> CallExpression:
        expression: CallExpression = CallExpression(function=function)
        expression.arguments = self.__parase_expression_list(TokenType.RPAREN)
        return expression

    def __parase_expression_list(self, end_token: TokenType) -> list[Expression]:
        expression_list: list[Expression] = []
        if self.__peek_token_is(end_token):
            self.__next_token()
            return expression_list
        self.__next_token() # skip lparen
        expression_list.append(self.__parse_expression(PrecedenceType.P_LOWEST))
        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()  # Skip comma
            self.__next_token()  # Parse the next element
            expression_list.append(self.__parse_expression(PrecedenceType.P_LOWEST))
        if not self.__expect_peek(end_token):
            return None
        return expression_list

    def __parse_identifier(self) -> IdentifierLiteral:
        return IdentifierLiteral(value=self.current_token.literal)

    def __parse_int_literal(self) -> Expression:
        integer_literal: IntegerLiteral = IntegerLiteral()
        try:
            integer_literal.value = int(self.current_token.literal)
        except:
            self.errors.append(f"Could Not Parse {self.current_token.literal} as Integer")
            return None
        return integer_literal

    def __parse_float_literal(self) -> Expression:
        float_literal: FloatLiteral = FloatLiteral()
        try:
            float_literal.value = float(self.current_token.literal)
        except:
            self.errors.append(f"Could Not Parse {self.current_token.literal} as Float")
            return None
        return float_literal

    def __parse_boolean(self) -> BooleanLiteral:
        return BooleanLiteral(value=self.__curent_token_is(TokenType.TRUE))

    def __parse_string_literal(self):
        value = self.current_token.literal
        return StringLiteral(value=value)

    def __parse_list_literal(self) -> ListLiteral:
        elements = []
        self.__next_token()
        if not self.__curent_token_is(TokenType.RBRACKET):
            elements.append(self.__parse_expression(PrecedenceType.P_LOWEST))
            while self.__peek_token_is(TokenType.COMMA):
                self.__next_token()
                self.__next_token()
                elements.append(self.__parse_expression(PrecedenceType.P_LOWEST))
        if not self.__expect_peek(TokenType.RBRACKET):
            return None
        return ListLiteral(elements=elements)
