#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>
#include <string.h>


// Function Pointer Type
typedef void (*OperationFunction)();

// #################### LEXER ####################

// ---------------- LEXER TYPEDEFS ------------------

typedef enum {
    TT_NULL,
    TT_PLUS,
    TT_MINUS,
    TT_ASTERISK,
    TT_SLASH,
    TT_POW,
    TT_MODULUS,
    TT_SEMICOLON,
    TT_LPAREN,
    TT_RPAREN,
    TT_ILLEGAL,
    TT_EOFTOKEN,
    TT_INT,
    TT_FLOAT
} TokenType;


typedef struct {
    TokenType type;
    union {
        char *str_value;  
        int int_value;    
        float float_value;
    } literal;
    uint32_t line_number;
    uint32_t position;
} Token;


typedef struct {
    char *code;
    uint32_t position;
    uint32_t read_position;        
    uint32_t line_number;
    char current_char;
} Lexer;

// ---------------- LEXER FUNCTIONS ------------------

void read_char(Lexer *lexer);
Lexer *new_lexer(char *code);
void free_lexer(Lexer *lexer);
void skip_whitespace(Lexer *lexer);
Token *new_token(Lexer *lexer, TokenType type, const char *literal);
Token *read_number(Lexer *lexer);
Token *next_lexer_token(Lexer *lexer);

void read_char(Lexer *lexer) {
    if (lexer->code[lexer->read_position] != '\0') {
        lexer->current_char = lexer->code[lexer->read_position];
    } else {
        lexer->current_char = '\0';
    }

    lexer->position = lexer->read_position;
    lexer->read_position += 1;
}

Lexer *new_lexer(char *code) {
    Lexer *lexer = malloc(sizeof(Lexer));
    lexer->code = code;
    lexer->position = -1;
    lexer->read_position = 0;
    lexer->line_number = 1;
    lexer->current_char = '\0';

    read_char(lexer);
    return lexer;
}

void free_lexer(Lexer *lexer) {
    free(lexer);
}

void skip_whitespace(Lexer *lexer) {
    while (
        lexer->current_char == ' ' || 
        lexer->current_char == '\t' || 
        lexer->current_char == '\n' || 
        lexer->current_char == '\r'
    ) {
        if (lexer->current_char == '\n') {
            lexer->line_number += 1;
        }
        read_char(lexer);
    }
}


Token *new_token(Lexer *lexer, TokenType type, const char *literal) {
    Token *token = malloc(sizeof(Token));
    token->type = type;

    if (type == TT_INT || type == TT_FLOAT) {
        // numbers already literals
    } else {
        // Allocate and copy string literal for ILLEGAL or others
        token->literal.str_value = malloc(strlen(literal) + 1);
        strcpy(token->literal.str_value, literal);
    }

    token->line_number = lexer->line_number;
    token->position = lexer->position;

    return token;
}


Token *read_number(Lexer *lexer) {
    uint32_t radix_point_count = 0;
    size_t buffer_size = 16;
    size_t length = 0;
    char *output = malloc(buffer_size);

    if (!output) {
        perror("Failed to allocate memory for number");
        exit(EXIT_FAILURE);
    }

    while (isdigit(lexer->current_char) || lexer->current_char == '.') {
        if (lexer->current_char == '.') {
            radix_point_count++;
        }

        if (radix_point_count > 1) {
            // Too many radix points
            fprintf(stderr, "Too many radix points at line %u, position %u\n",
                    lexer->line_number, lexer->position);
            
            output[length] = '\0';
            Token *token = new_token(lexer, TT_ILLEGAL, output);
            free(output);
            return token;
        }

        // Append the character to the buffer
        if (length + 1 >= buffer_size) {
            buffer_size *= 2;
            char *new_output = realloc(output, buffer_size);
            if (!new_output) {
                perror("Failed to reallocate memory for number");
                free(output);
                exit(EXIT_FAILURE);
            }
            output = new_output;
        }

        output[length++] = lexer->current_char;
        read_char(lexer);
    }

    output[length] = '\0'; // Null-terminate
    Token *token = malloc(sizeof(Token));

    if (radix_point_count == 0) {
        token->type = TT_INT;
        token->literal.int_value = atoi(output);
        printf("My INT is %d\n", token->literal.int_value);
    } else {
        token->type = TT_FLOAT;
        token->literal.float_value = atof(output);
        printf("My FLOAT is %f\n", token->literal.float_value);
    }

    token->line_number = lexer->line_number;
    token->position = lexer->position;

    free(output);
    return token;
}

void print_token(Token *token)
{
    if (token->type == TT_INT) {
        printf("Token INT: %d (Line: %u, Pos: %u)\n",
               token->literal.int_value, token->line_number, token->position);
    } else if (token->type == TT_FLOAT) {
        printf("Token FLOAT: %f (Line: %u, Pos: %u)\n",
               token->literal.float_value, token->line_number, token->position);
    } else {
        printf("Token ILLEGAL: %s (Line: %u, Pos: %u)\n",
               token->literal.str_value, token->line_number, token->position);
        free(token->literal.str_value);
    }
}


Token *next_lexer_token(Lexer *lexer) {
    Token *token;

    skip_whitespace(lexer);

    switch (lexer->current_char) {
        case '+':
            token = new_token(lexer, TT_PLUS, "+");
            break;
        case '-':
            token = new_token(lexer, TT_MINUS, "-");
            break;
        case '*':
            token = new_token(lexer, TT_ASTERISK, "*");
            break;
        case '/':
            token = new_token(lexer, TT_SLASH, "/");
            break;
        case '^':
            token = new_token(lexer, TT_POW, "^");
            break;
        case '%':
            token = new_token(lexer, TT_MODULUS, "%");
            break;
        case ';':
            token = new_token(lexer, TT_SEMICOLON, ";");
            break;
        case '(':
            token = new_token(lexer, TT_LPAREN, "(");
            break;
        case ')':
            token = new_token(lexer, TT_RPAREN, ")");
            break;
        case '\0': // End of file
            token = new_token(lexer, EOF, "");
            break;
        default:
            if (isdigit(lexer->current_char)) {
                token = read_number(lexer);
            } else {
                char illegal[2] = {lexer->current_char, '\0'};
                token = new_token(lexer, TT_ILLEGAL, illegal);
            }
    }

    // print_token(token);
    read_char(lexer);
    return token;
}

// #################### AST ####################

// ---------------- AST TYPEDEFS ------------------

typedef enum {
    AST_NT_PROGRAM,
    AST_NT_EXPRESSION_STATEMENT,
    AST_NT_INFIX_EXPRESSION,
    AST_NT_INT_LITERAL,
    AST_NT_FLOAT_LITERAL
} ASTNodeType;


typedef struct {
    ASTNodeType type;
    // function pointer, todo: learn more about this
    char *(*to_json)(struct ASTNode *self);

} ASTNode;

typedef struct {
    ASTNode base;
    ASTNode **statements;
    size_t statement_count;
    size_t statement_capacity;
} ASTProgramNode;


typedef struct {
    ASTNode base;
    ASTNode *expr;

} ASTExpressionStatement;


typedef struct {
    ASTNode base;
    ASTNode *left;
    char operator; // i assume we pass the literal into this?
    ASTNode *right;
} ASTInfixExpressionNode;


typedef struct {
    ASTNode base;
    int value;
} ASTIntLiteral;

typedef struct {
    ASTNode base;
    float value;
} ASTFloatiteral;

// ---------------- AST FUNCTIONS ------------------

// program_to_json function here

ASTProgramNode *create_program_node()
{
    ASTProgramNode *node = malloc(sizeof(ASTProgramNode));
    node->base.type = AST_NT_PROGRAM;
    node->base.to_json = program_to_json;
    node->statement_count = 0;
    node->statement_capacity = 4;
    // why malloc ASTNode size and not statement node size?
    node->statements = malloc(node->statement_capacity * sizeof(ASTNode *))    
    return node;
}







// #################### PARSER ####################

// ---------------- PARSER TYPEDEFS ------------------

typedef enum {
    P_LOWEST,
    P_EQUALS,
    P_LESSGREATER,
    P_SUM, // + -
    P_PRODUCT, // * / % 
    P_EXPONENT, // ^
    P_PREFIX,
    P_CALL,
    P_INDEX,
} PrecedenceType;

PrecedenceType precedences[] = {
    [TT_PLUS] = P_SUM,
    [TT_MINUS] = P_SUM,
    [TT_SLASH] = P_PRODUCT,
    [TT_ASTERISK] = P_PRODUCT,
    [TT_MODULUS] = P_PRODUCT,
    [TT_POW] = P_EXPONENT
};

typedef enum {
    PARSER_ERROR_INVALID_SYNTAX
} ParserErrorCode;

const char *parser_error_message[] = {
    "Invalid Syntax Provided."
};

typedef struct {
    ParserErrorCode code;
    int line_number;
} ParserError;

typedef struct {
    Lexer *lexer;
    ParserError **errors;
    size_t error_count;
    size_t error_capacity; // to prevent buffer overflow

    Token *current_token;
    Token *peek_token;
} Parser;


// ---------------- PARSER ERROR HANDLING --------------

void throw_parser_error(Parser *parser, ParserErrorCode error_code, int line_number)
{
    // resize if needed
    if(parser->error_count == parser->error_capacity){
        parser->error_capacity *= 2;
        parser->errors = realloc(parser->errors, parser->error_capacity * sizeof(ParserError *));
        if(!parser->errors){
            perror("Failed To Reallocate Memory For Errors");
            exit(1);
        }
    }

    ParserError *error = malloc(sizeof(ParserError));
    if(!error){
        perror("Failed To Allocate Memory For a Parser Error");
        exit(1);
    }

    error->code = error_code;
    error->line_number = line_number;
    
    parser->errors[parser->error_count++] = error;
}

const char *get_parser_error_message(ParserErrorCode error_code)
{
    return parser_error_message[error_code];
}
void print_parser_error(const Parser *parser)
{
    for(size_t error_num = 0; error_num < parser->error_count; error_num++){
        ParserError *error = parser->errors[error_num];
        printf("Parser Error : [Line %d] %s .\n",
            error->line_number,
            get_parser_error_message(error->code)
        );

    }
}

void free_parser_errors(Parser *parser)
{
    for(size_t error_num = 0; error_num < parser->error_count; error_num++){
        free(parser->errors[error_num]);
    }
    free(parser->errors);
}

// ---------------- PARSER FUNCTIONS ------------------


void parse_int_literal(Parser *parser){}
void parse_float_literal(Parser *parser){}
void parse_grouped_expression(Parser *parser){}

OperationFunction prefix_parse_functions[] = {
    [TT_INT] = parse_int_literal,
    [TT_FLOAT] = parse_float_literal,
    [TT_LPAREN] = parse_grouped_expression
};


void parse_infix_expression(Parser *parser){}

OperationFunction infix_parse_functions[] = {
    [TT_PLUS] = parse_infix_expression,
    [TT_MINUS] = parse_infix_expression,
    [TT_SLASH] = parse_infix_expression,
    [TT_ASTERISK] = parse_infix_expression,
    [TT_POW] = parse_infix_expression,
    [TT_MODULUS] = parse_infix_expression    
};




void next_parser_token(Parser *parser)
{
    parser->current_token = parser->peek_token;
    parser->peek_token = next_lexer_token(parser->lexer);



}


Parser *new_parser(Lexer *lexer)
{
    Parser *parser = malloc(sizeof(Parser));

    parser->lexer = lexer;
    parser->error_count = 0;
    parser->error_capacity = 20;
    parser->errors = malloc(parser->error_capacity * sizeof(ParserError *));

    parser->current_token = new_token(parser->lexer, TT_NULL, '\0');
    parser->peek_token = new_token(parser->lexer, TT_NULL, '\0');

    next_parser_token(parser);
    next_parser_token(parser);

    return parser;
}





int main() {
    const char *filename = "tests/test1.c4";

    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Source File Not Found");
        return 1;
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);

    char *buffer = malloc(file_size + 1);
    if (!buffer) {
        perror("Failed to allocate memory for input file");
        fclose(file);
        return 1;
    }

    fread(buffer, 1, file_size, file);
    buffer[file_size] = '\0';
    fclose(file);

    printf("We read this from the file: %s\n", buffer);

    Lexer *lexer = new_lexer(buffer);
    free(buffer);


    Parser *parser = new_parser(lexer);
    free_lexer(lexer);




    free_parser_errors(parser);
    free(parser);

    return 0;
}
