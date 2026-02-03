#!/usr/bin/env python3
"""
Advanced parser for the Clarity programming language.
Implements the full syntax as defined in the language specification.
"""

import re
import sys
from enum import Enum
from typing import List, Dict, Any, Optional, Union


class TokenType(Enum):
    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    
    # Keywords
    FN = "FN"
    LET = "LET"
    VAR = "VAR"
    CONST = "CONST"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN"
    RETURN = "RETURN"
    MATCH = "MATCH"
    ASYNC = "ASYNC"
    AWAIT = "AWAIT"
    TRUE = "TRUE"
    FALSE = "FALSE"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"   # %
    ASSIGN = "ASSIGN"
    EQ = "EQ"           # ==
    NEQ = "NEQ"         # !=
    LT = "LT"           # <
    GT = "GT"           # >
    LTE = "LTE"         # <=
    GTE = "GTE"         # >=
    AND = "AND"         # &&
    OR = "OR"           # ||
    NOT = "NOT"         # !
    
    # Delimiters
    LPAREN = "LPAREN"       # (
    RPAREN = "RPAREN"       # )
    LBRACE = "LBRACE"       # {
    RBRACE = "RBRACE"       # }
    LBRACKET = "LBRACKET"   # [
    RBRACKET = "RBRACKET"   # ]
    COMMA = "COMMA"         # ,
    COLON = "COLON"         # :
    ARROW = "ARROW"         # ->
    DOT = "DOT"             # .
    SEMICOLON = "SEMICOLON" # ;
    
    # Other
    EOF = "EOF"


class Token:
    """Represents a lexical token in our language."""
    
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value}, {self.line}:{self.column})"


class Lexer:
    """Lexical analyzer for the Clarity language."""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 0
        
    def advance(self):
        """Move to the next character."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1
            
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self) -> Optional[str]:
        """Look at the next character without advancing position."""
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        """Skip over whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip over single-line comments."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def read_number(self) -> str:
        """Read a number token."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result
    
    def read_identifier(self) -> str:
        """Read an identifier token."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def read_string(self) -> str:
        """Read a string literal."""
        result = ''
        quote_char = self.current_char  # Store opening quote
        self.advance()  # Skip opening quote
        
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':  # Handle escape sequences
                self.advance()
                if self.current_char is not None:
                    result += self.current_char
                    self.advance()
            else:
                result += self.current_char
                self.advance()
        
        if self.current_char == quote_char:
            self.advance()  # Skip closing quote
        
        return result
    
    def get_next_token(self) -> Token:
        """Get the next token from the input."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Comments
            if self.current_char == '/' and self.peek() == '/':
                self.advance()  # skip first '/'
                self.advance()  # skip second '/'
                self.skip_comment()
                continue
            
            if self.current_char.isdigit():
                start_line, start_col = self.line, self.column
                value = self.read_number()
                return Token(TokenType.NUMBER, value, start_line, start_col)
            
            if self.current_char.isalpha() or self.current_char == '_':
                start_line, start_col = self.line, self.column
                value = self.read_identifier()
                
                # Check if it's a keyword
                keyword_map = {
                    'fn': TokenType.FN,
                    'let': TokenType.LET,
                    'var': TokenType.VAR,
                    'const': TokenType.CONST,
                    'if': TokenType.IF,
                    'else': TokenType.ELSE,
                    'while': TokenType.WHILE,
                    'for': TokenType.FOR,
                    'in': TokenType.IN,
                    'return': TokenType.RETURN,
                    'match': TokenType.MATCH,
                    'async': TokenType.ASYNC,
                    'await': TokenType.AWAIT,
                    'true': TokenType.TRUE,
                    'false': TokenType.FALSE,
                }
                
                token_type = keyword_map.get(value.lower(), TokenType.IDENTIFIER)
                return Token(token_type, value, start_line, start_col)
            
            if self.current_char in ['"', "'"]:
                start_line, start_col = self.line, self.column
                value = self.read_string()
                return Token(TokenType.STRING, value, start_line, start_col)
            
            # Multi-character operators
            if self.current_char == '=' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token(TokenType.ARROW, '->', self.line, self.column - 1)
            
            # Two-character operators
            if self.current_char == '-' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token(TokenType.ARROW, '->', self.line, self.column - 1)
            elif self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQ, '==', self.line, self.column - 1)
            elif self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NEQ, '!=', self.line, self.column - 1)
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LTE, '<=', self.line, self.column - 1)
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GTE, '>=', self.line, self.column - 1)
            elif self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(TokenType.AND, '&&', self.line, self.column - 1)
            elif self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(TokenType.OR, '||', self.line, self.column - 1)
            
            # Single character tokens
            char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '!': TokenType.NOT,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
                ';': TokenType.SEMICOLON,
            }
            
            if self.current_char in char_tokens:
                char = self.current_char
                start_line, start_col = self.line, self.column
                self.advance()
                return Token(char_tokens[char], char, start_line, start_col)
            
            # Unknown character
            raise Exception(f"Illegal character '{self.current_char}' at {self.line}:{self.column}")
        
        return Token(TokenType.EOF, '', self.line, self.column)


class ASTNode:
    """Base class for Abstract Syntax Tree nodes."""
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
        self.node_type = 'Program'


class FunctionDef(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params  # List of (name, type) tuples
        self.return_type = return_type
        self.body = body  # List of statements
        self.node_type = 'FunctionDef'


class VariableDecl(ASTNode):
    def __init__(self, mutable, name, var_type, value):
        self.mutable = mutable  # True for 'var', False for 'let'
        self.name = name
        self.var_type = var_type
        self.value = value
        self.node_type = 'VariableDecl'


class ConstantDecl(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.node_type = 'ConstantDecl'


class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.node_type = 'Assignment'


class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.node_type = 'BinaryOp'


class UnaryOp(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
        self.node_type = 'UnaryOp'


class IfExpr(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.node_type = 'IfExpr'


class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.node_type = 'WhileLoop'


class ForLoop(ASTNode):
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.node_type = 'ForLoop'


class ReturnStmt(ASTNode):
    def __init__(self, value):
        self.value = value
        self.node_type = 'ReturnStmt'


class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.node_type = 'FunctionCall'


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
        self.node_type = 'Identifier'


class Number(ASTNode):
    def __init__(self, value):
        self.value = int(value)
        self.node_type = 'Number'


class String(ASTNode):
    def __init__(self, value):
        self.value = value
        self.node_type = 'String'


class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value
        self.node_type = 'Boolean'


class MatchExpr(ASTNode):
    def __init__(self, expr, arms):
        self.expr = expr
        self.arms = arms  # List of (pattern, result) tuples
        self.node_type = 'MatchExpr'


class Parser:
    """Parser for the Clarity language."""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type: TokenType):
        """Consume a token of the expected type."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected token {token_type.name}, got {self.current_token.type.name}")
    
    def parse_program(self):
        """Parse the entire program."""
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:  # Skip None statements (like empty lines/comments)
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self):
        """Parse a single statement."""
        token_type = self.current_token.type
        
        if token_type == TokenType.FN:
            return self.parse_function_def()
        elif token_type == TokenType.LET:
            return self.parse_variable_decl(mutable=False)
        elif token_type == TokenType.VAR:
            return self.parse_variable_decl(mutable=True)
        elif token_type == TokenType.CONST:
            return self.parse_constant_decl()
        elif token_type == TokenType.IF:
            return self.parse_if_expr()
        elif token_type == TokenType.WHILE:
            return self.parse_while_loop()
        elif token_type == TokenType.FOR:
            return self.parse_for_loop()
        elif token_type == TokenType.RETURN:
            return self.parse_return_stmt()
        elif token_type == TokenType.MATCH:
            return self.parse_match_expr()
        elif token_type == TokenType.IDENTIFIER:
            # Could be assignment or expression
            ident_name = self.current_token.value
            next_pos = self.lexer.pos
            next_char = self.lexer.current_char
            next_token = self.lexer.get_next_token()  # Peek at next token
            
            # Restore position
            self.lexer.pos = next_pos
            self.lexer.current_char = next_char
            self.current_token = Token(TokenType.IDENTIFIER, ident_name, self.lexer.line, self.lexer.column)
            
            if next_token.type == TokenType.ASSIGN:
                # It's an assignment
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.ASSIGN)
                value = self.parse_expression()
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                return Assignment(ident_name, value)
            else:
                # It's an expression (could be function call)
                expr = self.parse_expression()
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                return expr
        else:
            expr = self.parse_expression()
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
            return expr
    
    def parse_function_def(self):
        """Parse a function definition."""
        self.eat(TokenType.FN)
        
        # Parse function name
        func_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parse parameters
        self.eat(TokenType.LPAREN)
        params = []
        if self.current_token.type != TokenType.RPAREN:
            while True:
                param_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.COLON)
                param_type = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                params.append((param_name, param_type))
                
                if self.current_token.type == TokenType.RPAREN:
                    break
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        
        # Parse return type (optional)
        return_type = None
        if self.current_token.type == TokenType.ARROW:
            self.eat(TokenType.ARROW)
            return_type = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
        
        # Parse function body
        self.eat(TokenType.LBRACE)
        body = []
        while self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        self.eat(TokenType.RBRACE)
        
        return FunctionDef(func_name, params, return_type, body)
    
    def parse_variable_decl(self, mutable: bool):
        """Parse a variable declaration."""
        if mutable:
            self.eat(TokenType.VAR)
        else:
            self.eat(TokenType.LET)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parse type annotation (optional)
        var_type = None
        if self.current_token.type == TokenType.COLON:
            self.eat(TokenType.COLON)
            var_type = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
        
        # Parse assignment
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return VariableDecl(mutable, name, var_type, value)
    
    def parse_constant_decl(self):
        """Parse a constant declaration."""
        self.eat(TokenType.CONST)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return ConstantDecl(name, value)
    
    def parse_if_expr(self):
        """Parse an if expression."""
        self.eat(TokenType.IF)
        condition = self.parse_expression()
        
        self.eat(TokenType.LBRACE)
        then_body = []
        while self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt is not None:
                then_body.append(stmt)
        self.eat(TokenType.RBRACE)
        
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            else_body = []
            while self.current_token.type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt is not None:
                    else_body.append(stmt)
            self.eat(TokenType.RBRACE)
        
        return IfExpr(condition, then_body, else_body)
    
    def parse_while_loop(self):
        """Parse a while loop."""
        self.eat(TokenType.WHILE)
        condition = self.parse_expression()
        
        self.eat(TokenType.LBRACE)
        body = []
        while self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        self.eat(TokenType.RBRACE)
        
        return WhileLoop(condition, body)
    
    def parse_for_loop(self):
        """Parse a for loop."""
        self.eat(TokenType.FOR)
        
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.IN)
        
        iterable = self.parse_expression()
        
        self.eat(TokenType.LBRACE)
        body = []
        while self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        self.eat(TokenType.RBRACE)
        
        return ForLoop(var_name, iterable, body)
    
    def parse_return_stmt(self):
        """Parse a return statement."""
        self.eat(TokenType.RETURN)
        
        value = None
        if self.current_token.type != TokenType.SEMICOLON and self.current_token.type != TokenType.RBRACE:
            value = self.parse_expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return ReturnStmt(value)
    
    def parse_match_expr(self):
        """Parse a match expression."""
        self.eat(TokenType.MATCH)
        expr = self.parse_expression()
        
        self.eat(TokenType.LBRACE)
        arms = []
        while self.current_token.type != TokenType.RBRACE:
            # Parse pattern (simplified - just identifiers or literals for now)
            if self.current_token.type in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING]:
                pattern = self.parse_primary()
            else:
                raise Exception(f"Invalid pattern in match at {self.current_token.line}:{self.current_token.column}")
            
            self.eat(TokenType.ARROW)  # =>
            result = self.parse_expression()
            
            arms.append((pattern, result))
            
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            elif self.current_token.type == TokenType.RBRACE:
                break
            else:
                raise Exception(f"Expected comma or closing brace in match expression at {self.current_token.line}:{self.current_token.column}")
        
        self.eat(TokenType.RBRACE)
        
        return MatchExpr(expr, arms)
    
    def parse_expression(self):
        """Parse an expression with operator precedence."""
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        """Parse logical OR expressions."""
        left = self.parse_logical_and()
        
        while self.current_token.type == TokenType.OR:
            op = self.current_token
            self.eat(TokenType.OR)
            right = self.parse_logical_and()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_logical_and(self):
        """Parse logical AND expressions."""
        left = self.parse_equality()
        
        while self.current_token.type == TokenType.AND:
            op = self.current_token
            self.eat(TokenType.AND)
            right = self.parse_equality()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_equality(self):
        """Parse equality expressions."""
        left = self.parse_comparison()
        
        while self.current_token.type in [TokenType.EQ, TokenType.NEQ]:
            op = self.current_token
            if op.type == TokenType.EQ:
                self.eat(TokenType.EQ)
            else:
                self.eat(TokenType.NEQ)
            right = self.parse_comparison()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_comparison(self):
        """Parse comparison expressions."""
        left = self.parse_term()
        
        while self.current_token.type in [TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE]:
            op = self.current_token
            if op.type == TokenType.LT:
                self.eat(TokenType.LT)
            elif op.type == TokenType.GT:
                self.eat(TokenType.GT)
            elif op.type == TokenType.LTE:
                self.eat(TokenType.LTE)
            else:  # GTE
                self.eat(TokenType.GTE)
            right = self.parse_term()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_term(self):
        """Parse addition and subtraction."""
        left = self.parse_factor()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token
            if op.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:  # MINUS
                self.eat(TokenType.MINUS)
            right = self.parse_factor()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_factor(self):
        """Parse multiplication and division."""
        left = self.parse_unary()
        
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token
            if op.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            else:  # DIVIDE
                self.eat(TokenType.DIVIDE)
            right = self.parse_unary()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_unary(self):
        """Parse unary operators."""
        if self.current_token.type in [TokenType.MINUS, TokenType.NOT]:
            op = self.current_token
            if op.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            else:  # NOT
                self.eat(TokenType.NOT)
            operand = self.parse_unary()
            return UnaryOp(op.value, operand)
        
        return self.parse_call()
    
    def parse_call(self):
        """Parse function calls and primary expressions."""
        expr = self.parse_primary()
        
        while self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            args = []
            if self.current_token.type != TokenType.RPAREN:
                while True:
                    args.append(self.parse_expression())
                    if self.current_token.type == TokenType.RPAREN:
                        break
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RPAREN)
            expr = FunctionCall(expr.name if hasattr(expr, 'name') else expr.value, args)
        
        return expr
    
    def parse_primary(self):
        """Parse primary expressions (literals, identifiers, parenthesized expressions)."""
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(True)
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(False)
        elif token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            return Identifier(name)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            raise Exception(f"Unexpected token: {token.type.name}")


def main():
    """Main function for testing the parser."""
    print("Clarity Language Parser")
    print("Enter Clarity code to parse, or press Ctrl+C to exit.\n")
    
    # Test with a sample Clarity program
    sample_code = '''
    fn main() {
        let x: Int = 42;
        var y = x + 10;
        if x > 40 {
            println("x is greater than 40");
        } else {
            println("x is not greater than 40");
        }
        return y;
    }
    '''
    
    print("Parsing sample code:")
    print(sample_code)
    print("\nTokens:")
    
    lexer = Lexer(sample_code)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        print(token)
        if token.type == TokenType.EOF:
            break
    
    print("\nParsing AST:")
    lexer = Lexer(sample_code)
    parser = Parser(lexer)
    try:
        ast = parser.parse_program()
        print_ast(ast, 0)
    except Exception as e:
        print(f"Parse error: {e}")


def print_ast(node, depth=0):
    """Helper function to print the AST in a readable format."""
    indent = "  " * depth
    if isinstance(node, Program):
        print(f"{indent}Program")
        for stmt in node.statements:
            print_ast(stmt, depth + 1)
    elif isinstance(node, FunctionDef):
        print(f"{indent}FunctionDef: {node.name}")
        print(f"{indent}  Params: {node.params}")
        print(f"{indent}  ReturnType: {node.return_type}")
        print(f"{indent}  Body:")
        for stmt in node.body:
            print_ast(stmt, depth + 2)
    elif isinstance(node, VariableDecl):
        mut = "mut" if node.mutable else "let"
        print(f"{indent}VariableDecl: {mut} {node.name}: {node.var_type} = ")
        print_ast(node.value, depth + 1)
    elif isinstance(node, BinaryOp):
        print(f"{indent}BinaryOp: {node.operator}")
        print_ast(node.left, depth + 1)
        print_ast(node.right, depth + 1)
    elif isinstance(node, Identifier):
        print(f"{indent}Identifier: {node.name}")
    elif isinstance(node, Number):
        print(f"{indent}Number: {node.value}")
    elif isinstance(node, String):
        print(f"{indent}String: {node.value}")
    elif isinstance(node, IfExpr):
        print(f"{indent}IfExpr")
        print(f"{indent}  Condition:")
        print_ast(node.condition, depth + 1)
        print(f"{indent}  Then:")
        for stmt in node.then_branch:
            print_ast(stmt, depth + 1)
        if node.else_branch:
            print(f"{indent}  Else:")
            for stmt in node.else_branch:
                print_ast(stmt, depth + 1)
    else:
        print(f"{indent}{node.node_type}: {getattr(node, 'name', getattr(node, 'value', 'Unknown'))}")


if __name__ == '__main__':
    main()