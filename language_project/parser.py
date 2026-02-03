#!/usr/bin/env python3
"""
Basic parser for our new programming language.
This is a placeholder that will be expanded as we design the language.
"""

import re
import sys
from typing import List, Dict, Any, Optional


class Token:
    """Represents a lexical token in our language."""
    
    def __init__(self, type_: str, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"


class Lexer:
    """Lexical analyzer for our language."""
    
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
                    result += '\\' + self.current_char
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
            
            if self.current_char.isdigit():
                start_line, start_col = self.line, self.column
                value = self.read_number()
                return Token('NUMBER', value, start_line, start_col)
            
            if self.current_char.isalpha() or self.current_char == '_':
                start_line, start_col = self.line, self.column
                value = self.read_identifier()
                
                # Check if it's a keyword
                if value in ['if', 'else', 'while', 'for', 'def', 'return']:
                    return Token(value.upper(), value, start_line, start_col)
                
                return Token('IDENTIFIER', value, start_line, start_col)
            
            if self.current_char in ['"', "'"]:
                start_line, start_col = self.line, self.column
                value = self.read_string()
                return Token('STRING', value, start_line, start_col)
            
            # Single character tokens
            if self.current_char in '+-*/=<>!&|':
                op = self.current_char
                start_line, start_col = self.line, self.column
                self.advance()
                
                # Check for double-character operators
                if op == '=' and self.current_char == '=':
                    self.advance()
                    return Token('EQ', '==', start_line, start_col)
                elif op == '!' and self.current_char == '=':
                    self.advance()
                    return Token('NEQ', '!=', start_line, start_col)
                elif op == '<' and self.current_char == '=':
                    self.advance()
                    return Token('LTE', '<=', start_line, start_col)
                elif op == '>' and self.current_char == '=':
                    self.advance()
                    return Token('GTE', '>=', start_line, start_col)
                elif op == '&' and self.current_char == '&':
                    self.advance()
                    return Token('AND', '&&', start_line, start_col)
                elif op == '|' and self.current_char == '|':
                    self.advance()
                    return Token('OR', '||', start_line, start_col)
                
                return Token(op, op, start_line, start_col)
            
            # Parentheses, braces, brackets
            if self.current_char in '(){}[]':
                char = self.current_char
                start_line, start_col = self.line, self.column
                self.advance()
                return Token(char, char, start_line, start_col)
            
            # Other symbols
            if self.current_char in ',;:.':
                char = self.current_char
                start_line, start_col = self.line, self.column
                self.advance()
                return Token(char, char, start_line, start_col)
            
            # Unknown character
            raise Exception(f"Illegal character '{self.current_char}' at {self.line}:{self.column}")
        
        return Token('EOF', '', self.line, self.column)


class Parser:
    """Parser for our language."""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type: str):
        """Consume a token of the expected type."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected token {token_type}, got {self.current_token.type}")
    
    def factor(self):
        """Parse a factor (numbers, variables, parenthesized expressions)."""
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return {'type': 'number', 'value': int(token.value)}
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return {'type': 'identifier', 'name': token.value}
        elif token.type == '(':
            self.eat('(')
            result = self.expression()
            self.eat(')')
            return result
        else:
            raise Exception(f"Unexpected token: {token.type}")
    
    def term(self):
        """Parse a term (multiplication and division)."""
        node = self.factor()
        
        while self.current_token.type in ['*', '/']:
            op = self.current_token
            if op.type == '*':
                self.eat('*')
            elif op.type == '/':
                self.eat('/')
            
            node = {
                'type': 'binary_op',
                'operator': op.value,
                'left': node,
                'right': self.factor()
            }
        
        return node
    
    def expression(self):
        """Parse an expression (addition and subtraction)."""
        node = self.term()
        
        while self.current_token.type in ['+', '-']:
            op = self.current_token
            if op.type == '+':
                self.eat('+')
            elif op.type == '-':
                self.eat('-')
            
            node = {
                'type': 'binary_op',
                'operator': op.value,
                'left': node,
                'right': self.term()
            }
        
        return node
    
    def parse(self):
        """Parse the entire input."""
        return self.expression()


def main():
    """Main function for testing the parser."""
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            text = file.read()
    else:
        text = input("Enter expression: ")
    
    lexer = Lexer(text)
    
    print("Tokens:")
    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type == 'EOF':
            break
    
    # Reset lexer to parse the expression
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()
    
    print("\nAST:")
    import pprint
    pprint.pprint(ast)


if __name__ == '__main__':
    main()