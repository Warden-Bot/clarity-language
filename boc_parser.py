#!/usr/bin/env python3
"""
Parser for Bot-Optimized Clarity (BOC) - a language designed for AI agents to communicate
and reason with each other.
"""

import re
import json
from enum import Enum
from typing import List, Dict, Any, Optional, Union


class BOCTokenType(Enum):
    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Keywords
    BELIEF = "BELIEF"
    REASONING_CONTEXT = "REASONING_CONTEXT"
    INTENT = "INTENT"
    SHARED_STATE = "SHARED_STATE"
    SELF_CAPABILITY = "SELF_CAPABILITY"
    CALCULATE_WITH_UNCERTAINTY = "CALCULATE_WITH_UNCERTAINTY"
    STRUCTURED_KNOWLEDGE = "STRUCTURED_KNOWLEDGE"
    ENTITY = "ENTITY"
    AT = "AT"
    TIMESTAMP = "TIMESTAMP"
    
    # Operators
    ASSIGN = "ASSIGN"      # =
    LAMBDA = "LAMBDA"      # =>
    ACCESS = "ACCESS"      # .
    RANGE = "RANGE"        # ..
    
    # Delimiters
    LBRACE = "LBRACE"       # {
    RBRACE = "RBRACE"       # }
    LBRACKET = "LBRACKET"   # [
    RBRACKET = "RBRACKET"   # ]
    LPAREN = "LPAREN"       # (
    RPAREN = "RPAREN"       # )
    COMMA = "COMMA"         # ,
    COLON = "COLON"         # :
    SEMICOLON = "SEMICOLON" # ;
    
    # Special
    EOF = "EOF"


class BOCNode:
    """Base class for BOC AST nodes."""
    pass


class BOCToken:
    """Represents a lexical token in BOC."""
    
    def __init__(self, type_: BOCTokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"BOCToken({self.type.name}, {self.value}, {self.line}:{self.column})"


class BOCLexer:
    """Lexical analyzer for Bot-Optimized Clarity."""
    
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
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return result
    
    def read_identifier(self) -> str:
        """Read an identifier token."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ['_', '-', '@']):
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
    
    def get_next_token(self) -> BOCToken:
        """Get the next token from the input."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                start_line, start_col = self.line, self.column
                value = self.read_number()
                return BOCToken(BOCTokenType.NUMBER, value, start_line, start_col)
            
            if self.current_char.isalpha() or self.current_char == '@':
                start_line, start_col = self.line, self.column
                value = self.read_identifier()
                
                # Check if it's a keyword
                keyword_map = {
                    'belief': BOCTokenType.BELIEF,
                    'reasoning_context': BOCTokenType.REASONING_CONTEXT,
                    'intent': BOCTokenType.INTENT,
                    'shared_state': BOCTokenType.SHARED_STATE,
                    'self_capability': BOCTokenType.SELF_CAPABILITY,
                    'calculate_with_uncertainty': BOCTokenType.CALCULATE_WITH_UNCERTAINTY,
                    'structured_knowledge': BOCTokenType.STRUCTURED_KNOWLEDGE,
                    'entity': BOCTokenType.ENTITY,
                    'true': BOCTokenType.BOOLEAN,
                    'false': BOCTokenType.BOOLEAN,
                }
                
                token_type = keyword_map.get(value.lower(), BOCTokenType.IDENTIFIER)
                return BOCToken(token_type, value, start_line, start_col)
            
            if self.current_char in ['"', "'"]:
                start_line, start_col = self.line, self.column
                value = self.read_string()
                return BOCToken(BOCTokenType.STRING, value, start_line, start_col)
            
            # Multi-character operators
            if self.current_char == '.' and self.peek() == '.':
                self.advance()
                self.advance()
                return BOCToken(BOCTokenType.RANGE, '..', self.line, self.column - 1)
            
            if self.current_char == '=' and self.peek() == '>':
                self.advance()
                self.advance()
                return BOCToken(BOCTokenType.LAMBDA, '=>', self.line, self.column - 1)
            
            # Single character tokens
            char_tokens = {
                '=': BOCTokenType.ASSIGN,
                '{': BOCTokenType.LBRACE,
                '}': BOCTokenType.RBRACE,
                '[': BOCTokenType.LBRACKET,
                ']': BOCTokenType.RBRACKET,
                '(': BOCTokenType.LPAREN,
                ')': BOCTokenType.RPAREN,
                ',': BOCTokenType.COMMA,
                ':': BOCTokenType.COLON,
                '.': BOCTokenType.ACCESS,
                ';': BOCTokenType.SEMICOLON,
                '@': BOCTokenType.AT,
            }
            
            if self.current_char in char_tokens:
                char = self.current_char
                start_line, start_col = self.line, self.column
                self.advance()
                return BOCToken(char_tokens[char], char, start_line, start_col)
            
            # Unknown character
            raise Exception(f"Illegal character '{self.current_char}' at {self.line}:{self.column}")
        
        return BOCToken(BOCTokenType.EOF, '', self.line, self.column)


class BOCBelief(BOCNode):
    def __init__(self, attributes, content):
        self.attributes = attributes  # dict of attribute_name -> value
        self.content = content        # list of statements/content
        self.node_type = 'BOCBelief'


class BOCReasoningContext(BOCNode):
    def __init__(self, attributes, content):
        self.attributes = attributes
        self.content = content
        self.node_type = 'BOCReasoningContext'


class BOCIntent(BOCNode):
    def __init__(self, action, attributes, content):
        self.action = action
        self.attributes = attributes
        self.content = content
        self.node_type = 'BOCIntent'


class BOCStructuredKnowledge(BOCNode):
    def __init__(self, attributes, content):
        self.attributes = attributes
        self.content = content
        self.node_type = 'BOCStructuredKnowledge'


class BOCParser:
    """Parser for Bot-Optimized Clarity."""
    
    def __init__(self, lexer: BOCLexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type: BOCTokenType):
        """Consume a token of the expected type."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected token {token_type.name}, got {self.current_token.type.name}")
    
    def parse_program(self):
        """Parse the entire program."""
        statements = []
        while self.current_token.type != BOCTokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return {'type': 'BOCProgram', 'statements': statements}
    
    def parse_statement(self):
        """Parse a single statement."""
        token_type = self.current_token.type
        
        if token_type == BOCTokenType.BELIEF:
            return self.parse_belief()
        elif token_type == BOCTokenType.REASONING_CONTEXT:
            return self.parse_reasoning_context()
        elif token_type == BOCTokenType.INTENT:
            return self.parse_intent()
        elif token_type == BOCTokenType.SHARED_STATE:
            return self.parse_shared_state()
        elif token_type == BOCTokenType.SELF_CAPABILITY:
            return self.parse_self_capability()
        elif token_type == BOCTokenType.CALCULATE_WITH_UNCERTAINTY:
            return self.parse_calculate_with_uncertainty()
        elif token_type == BOCTokenType.STRUCTURED_KNOWLEDGE:
            return self.parse_structured_knowledge()
        elif token_type == BOCTokenType.IDENTIFIER:
            return self.parse_assignment()
        else:
            raise Exception(f"Unexpected statement starting with {token_type.name}")
    
    def parse_shared_state(self):
        """Parse a shared state statement."""
        self.eat(BOCTokenType.SHARED_STATE)
        attributes = self.parse_attributes()
        content = self.parse_block_content()
        return {'type': 'SharedState', 'attributes': attributes, 'content': content}
    
    def parse_self_capability(self):
        """Parse a self capability statement."""
        self.eat(BOCTokenType.SELF_CAPABILITY)
        attributes = self.parse_attributes()
        content = self.parse_block_content()
        return {'type': 'SelfCapability', 'attributes': attributes, 'content': content}
    
    def parse_calculate_with_uncertainty(self):
        """Parse a calculate with uncertainty statement."""
        self.eat(BOCTokenType.CALCULATE_WITH_UNCERTAINTY)
        attributes = self.parse_attributes()
        content = self.parse_block_content()
        return {'type': 'CalculateWithUncertainty', 'attributes': attributes, 'content': content}
    
    def parse_attributes(self):
        """Parse attribute list like @attr1(...) @attr2(...)"""
        attributes = {}
        while self.current_token.type == BOCTokenType.AT:
            self.eat(BOCTokenType.AT)
            attr_name = self.current_token.value
            self.eat(BOCTokenType.IDENTIFIER)
            
            if self.current_token.type == BOCTokenType.LPAREN:
                self.eat(BOCTokenType.LPAREN)
                attr_value = self.parse_expression()
                self.eat(BOCTokenType.RPAREN)
            else:
                attr_value = True  # Attribute without value is treated as true
                
            attributes[attr_name] = attr_value
        
        return attributes
    
    def parse_block_content(self):
        """Parse content inside braces { ... }"""
        content = []
        self.eat(BOCTokenType.LBRACE)
        
        while self.current_token.type != BOCTokenType.RBRACE:
            if self.current_token.type == BOCTokenType.IDENTIFIER:
                # Parse key-value pairs like: key: value
                key = self.current_token.value
                self.eat(BOCTokenType.IDENTIFIER)
                self.eat(BOCTokenType.COLON)
                value = self.parse_expression()
                content.append({'type': 'KeyValue', 'key': key, 'value': value})
            elif self.current_token.type == BOCTokenType.RBRACE:
                break
            else:
                # Try to parse as a general expression
                expr = self.parse_expression()
                content.append(expr)
        
        self.eat(BOCTokenType.RBRACE)
        return content
    
    def parse_belief(self):
        """Parse a belief statement."""
        self.eat(BOCTokenType.BELIEF)
        
        # Parse optional attributes like confidence=0.85
        attributes = {}
        if self.current_token.type == BOCTokenType.IDENTIFIER and self.current_token.value == 'confidence':
            self.eat(BOCTokenType.IDENTIFIER)  # confidence
            self.eat(BOCTokenType.ASSIGN)
            confidence_value = self.parse_expression()
            attributes['confidence'] = confidence_value
        
        content = self.parse_block_content()
        return BOCBelief(attributes, content)
    
    def parse_reasoning_context(self):
        """Parse a reasoning context."""
        self.eat(BOCTokenType.REASONING_CONTEXT)
        attributes = self.parse_attributes()
        content = self.parse_block_content()
        return BOCReasoningContext(attributes, content)
    
    def parse_intent(self):
        """Parse an intent statement."""
        self.eat(BOCTokenType.INTENT)
        
        # Parse action if present (like "to_perform: action_name")
        action = None
        if self.current_token.type == BOCTokenType.IDENTIFIER and self.current_token.value in ['to_perform']:
            action_type = self.current_token.value
            self.eat(BOCTokenType.IDENTIFIER)
            self.eat(BOCTokenType.COLON)
            # Action value can be any expression (string, identifier, etc.)
            action_value = self.parse_expression()
            action = {'type': action_type, 'value': action_value}
        
        attributes = self.parse_attributes()
        content = self.parse_block_content()
        return BOCIntent(action, attributes, content)
    
    def parse_structured_knowledge(self):
        """Parse structured knowledge."""
        self.eat(BOCTokenType.STRUCTURED_KNOWLEDGE)
        attributes = self.parse_attributes()
        content = self.parse_block_content()
        return BOCStructuredKnowledge(attributes, content)
    
    def parse_assignment(self):
        """Parse a simple assignment."""
        key = self.current_token.value
        self.eat(BOCTokenType.IDENTIFIER)
        self.eat(BOCTokenType.ASSIGN)
        value = self.parse_expression()
        return {'type': 'Assignment', 'key': key, 'value': value}
    
    def parse_expression(self):
        """Parse an expression."""
        # Handle array expressions first
        if self.current_token.type == BOCTokenType.LBRACKET:
            return self.parse_array()
        
        # For now, just handle basic expressions
        if self.current_token.type in [BOCTokenType.STRING, BOCTokenType.NUMBER, BOCTokenType.BOOLEAN]:
            value = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)
            return {'type': 'Literal', 'value': value, 'token_type': token_type.name}
        elif self.current_token.type == BOCTokenType.IDENTIFIER:
            value = self.current_token.value
            self.eat(BOCTokenType.IDENTIFIER)
            return {'type': 'Identifier', 'value': value}
        else:
            raise Exception(f"Unexpected token in expression: {self.current_token.type.name}")
    
    def parse_array(self):
        """Parse an array expression [item1, item2, ...]"""
        self.eat(BOCTokenType.LBRACKET)
        items = []
        
        if self.current_token.type != BOCTokenType.RBRACKET:
            while True:
                item = self.parse_expression()
                items.append(item)
                
                if self.current_token.type == BOCTokenType.RBRACKET:
                    break
                elif self.current_token.type == BOCTokenType.COMMA:
                    self.eat(BOCTokenType.COMMA)
                else:
                    raise Exception(f"Expected comma or closing bracket, got {self.current_token.type.name}")
        
        self.eat(BOCTokenType.RBRACKET)
        return {'type': 'Array', 'items': items}


def parse_boc_code(code: str):
    """Parse BOC code and return the AST."""
    lexer = BOCLexer(code)
    parser = BOCParser(lexer)
    return parser.parse_program()


def main():
    """Test the BOC parser with sample code."""
    sample_boc_code = """
    belief confidence=0.85 {
        fact: "temperature_in_celsius(22.5)"
        source: "sensor_123"
        time: "2026-02-02T19:00:00Z"
    }
    
    intent to_perform: "coordinate_meeting_arrangements" {
        participants: ["agent_a", "agent_b", "agent_c"]
        time_window: "2026-02-03T10:00:00Z/16:00:00Z"
        confidence_level: 0.9
    }
    """
    
    print("Sample BOC Code:")
    print(sample_boc_code)
    print("\nParsing...")
    
    try:
        ast = parse_boc_code(sample_boc_code)
        print("\nParsed AST:")
        print(json.dumps(ast, indent=2, default=str))
    except Exception as e:
        print(f"\nParse error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()