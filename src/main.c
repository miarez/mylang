#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>
#include <string.h>


typedef enum {
    PLUS,
    MINUS,
    ASTERISK,
    SLASH,
    POW,
    MODULUS,
    SEMICOLON,
    LPAREN,
    RPAREN,
    ILLEGAL,
    EOFTOKEN,
    INT,
    FLOAT
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

// Function prototypes
void read_char(Lexer *lexer);
Lexer *new_lexer(char *code);
void free_lexer(Lexer *lexer);
void skip_whitespace(Lexer *lexer);
Token *new_token(Lexer *lexer, TokenType type, const char *literal);
Token *read_number(Lexer *lexer);
void next_token(Lexer *lexer);


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

    if (type == INT || type == FLOAT) {
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
            Token *token = new_token(lexer, ILLEGAL, output);
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
        token->type = INT;
        token->literal.int_value = atoi(output);
        printf("My INT is %d\n", token->literal.int_value);
    } else {
        token->type = FLOAT;
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
    if (token->type == INT) {
        printf("Token INT: %d (Line: %u, Pos: %u)\n",
               token->literal.int_value, token->line_number, token->position);
    } else if (token->type == FLOAT) {
        printf("Token FLOAT: %f (Line: %u, Pos: %u)\n",
               token->literal.float_value, token->line_number, token->position);
    } else {
        printf("Token ILLEGAL: %s (Line: %u, Pos: %u)\n",
               token->literal.str_value, token->line_number, token->position);
        free(token->literal.str_value);
    }
}


void next_token(Lexer *lexer) {
    Token *token;

    skip_whitespace(lexer);

    switch (lexer->current_char) {
        case '+':
            token = new_token(lexer, PLUS, "+");
            break;
        case '-':
            token = new_token(lexer, MINUS, "-");
            break;
        case '*':
            token = new_token(lexer, ASTERISK, "*");
            break;
        case '/':
            token = new_token(lexer, SLASH, "/");
            break;
        case '^':
            token = new_token(lexer, POW, "^");
            break;
        case '%':
            token = new_token(lexer, MODULUS, "%");
            break;
        case ';':
            token = new_token(lexer, SEMICOLON, ";");
            break;
        case '(':
            token = new_token(lexer, LPAREN, "(");
            break;
        case ')':
            token = new_token(lexer, RPAREN, ")");
            break;
        case '\0': // End of file
            token = new_token(lexer, EOF, "");
            break;
        default:
            if (isdigit(lexer->current_char)) {
                token = read_number(lexer);
            } else {
                char illegal[2] = {lexer->current_char, '\0'};
                token = new_token(lexer, ILLEGAL, illegal);
            }
    }

    print_token(token);

    free(token);
    read_char(lexer);
}

int main() {
    const char *filename = "tests/test0.c4";

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

    while (lexer->current_char != '\0') {
        next_token(lexer);
    }

    free(buffer);
    free_lexer(lexer);

    return 0;
}
