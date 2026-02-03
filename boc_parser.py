#!/usr/bin/env python3
"""
Parser for Bot-Optimized Clarity (BOC) - a language designed for AI agents to communicate
and reason with each other.
"""

import re
import json
from enum import Enum
from typing import List, Dict, Any, Optional, Union
from uncertainty_propagation import UncertaintyValue, UncertaintyPropagator, UncertaintyType
from belief_management import BeliefManager, Evidence, EvidenceType, DecayFunction


class BOCTokenType(Enum):
    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    UNCERTAINTY = "UNCERTAINTY"  # ± value notation
    
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
    UPDATE_BELIEF = "UPDATE_BELIEF"
    CONFIDENCE_DECAY = "CONFIDENCE_DECAY"
    AGENT_COORDINATION = "AGENT_COORDINATION"
    PROVENANCE = "PROVENANCE"
    
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
    
    def skip_comment(self):
        """Skip over single-line comments."""
        while self.current_char is not None and self.current_char != '\n':
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
            
            # Comments
            if self.current_char == '/' and self.peek() == '/':
                self.advance()  # skip first '/'
                self.advance()  # skip second '/'
                self.skip_comment()
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
                    'update_belief': BOCTokenType.UPDATE_BELIEF,
                    'confidence_decay': BOCTokenType.CONFIDENCE_DECAY,
                    'agent_coordination': BOCTokenType.AGENT_COORDINATION,
                    'provenance': BOCTokenType.PROVENANCE,
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

            # Uncertainty notation ±
            if self.current_char == '±':
                start_line, start_col = self.line, self.column
                self.advance()
                # Read the uncertainty value
                uncertainty_value = ''
                while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                    uncertainty_value += self.current_char
                    self.advance()
                return BOCToken(BOCTokenType.UNCERTAINTY, f'±{uncertainty_value}', start_line, start_col)
            
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


class BOCUpdateBelief(BOCNode):
    def __init__(self, belief_name, new_confidence, evidence_source, evidence_type=None):
        self.belief_name = belief_name
        self.new_confidence = new_confidence
        self.evidence_source = evidence_source
        self.evidence_type = evidence_type or EvidenceType.NEUTRAL
        self.node_type = 'BOCUpdateBelief'
        
        # Create evidence object for belief manager
        from datetime import datetime
        self.evidence = Evidence(
            content=f"Belief update to {new_confidence}",
            confidence=new_confidence,
            source=evidence_source or "unknown",
            timestamp=datetime.now(),
            evidence_type=self.evidence_type,
            weight=1.0
        )
    
    def apply_to_manager(self, belief_manager: BeliefManager) -> bool:
        """Apply this belief update to a belief manager."""
        try:
            # Extract confidence value if it's a dictionary
            confidence = self.new_confidence
            if isinstance(confidence, dict) and 'value' in confidence:
                confidence = float(confidence['value'])
            elif isinstance(confidence, str):
                confidence = float(confidence)
            
            return belief_manager.update_belief(
                self.belief_name, 
                confidence,
                self.evidence
            )
        except (ValueError, TypeError):
            return False


class BOCConfidenceDecay(BOCNode):
    def __init__(self, belief_name, decay_function, time_period):
        self.belief_name = belief_name
        self.decay_function = decay_function
        self.time_period = time_period
        self.node_type = 'BOCConfidenceDecay'
        
        # Parse decay function and period
        self.parsed_decay_function = self._parse_decay_function(decay_function)
        self.parsed_period = self._parse_time_period(time_period)
    
    def _parse_decay_function(self, decay_func):
        """Parse decay function string to DecayFunction enum."""
        if isinstance(decay_func, str):
            decay_lower = decay_func.lower()
            if 'exponential' in decay_lower:
                rate = self._extract_rate(decay_func)
                return (DecayFunction.EXPONENTIAL, rate)
            elif 'linear' in decay_lower:
                rate = self._extract_rate(decay_func)
                return (DecayFunction.LINEAR, rate)
            elif 'logarithmic' in decay_lower:
                rate = self._extract_rate(decay_func)
                return (DecayFunction.LOGARITHMIC, rate)
            elif 'step' in decay_lower:
                rate = self._extract_rate(decay_func)
                return (DecayFunction.STEP, rate)
        
        return (DecayFunction.EXPONENTIAL, 0.1)  # Default
    
    def _parse_time_period(self, time_period):
        """Parse time period string to timedelta."""
        if isinstance(time_period, str):
            if 'day' in time_period.lower():
                days = self._extract_number(time_period)
                from datetime import timedelta
                return timedelta(days=days)
            elif 'hour' in time_period.lower():
                hours = self._extract_number(time_period)
                from datetime import timedelta
                return timedelta(hours=hours)
            elif 'minute' in time_period.lower():
                minutes = self._extract_number(time_period)
                from datetime import timedelta
                return timedelta(minutes=minutes)
        
        from datetime import timedelta
        return timedelta(hours=1)  # Default
    
    def _extract_rate(self, func_str):
        """Extract decay rate from function string."""
        import re
        match = re.search(r'(\d+\.?\d*)', func_str)
        return float(match.group(1)) if match else 0.1
    
    def _extract_number(self, period_str):
        """Extract number from period string."""
        import re
        match = re.search(r'(\d+\.?\d*)', period_str)
        return float(match.group(1)) if match else 1.0
    
    def apply_to_manager(self, belief_manager: BeliefManager) -> bool:
        """Apply this confidence decay to a belief manager."""
        try:
            if self.belief_name in belief_manager.beliefs:
                belief = belief_manager.beliefs[self.belief_name]
                belief.decay_function = self.parsed_decay_function[0]
                belief.decay_rate = self.parsed_decay_function[1]
                belief.decay_period = self.parsed_period
                return True
        except Exception:
            pass
        
        return False


class BOCAgentCoordination(BOCNode):
    def __init__(self, coordinator, participants, coordination_type, constraints):
        self.coordinator = coordinator
        self.participants = participants
        self.coordination_type = coordination_type
        self.constraints = constraints
        self.node_type = 'BOCAgentCoordination'


class BOCProvenance(BOCNode):
    def __init__(self, source, timestamp, chain_of_custody):
        self.source = source
        self.timestamp = timestamp
        self.chain_of_custody = chain_of_custody
        self.node_type = 'BOCProvenance'


class BOCUncertainty(BOCNode):
    def __init__(self, value, uncertainty_range, uncertainty_value=None):
        self.value = value
        self.uncertainty_range = uncertainty_range
        self.uncertainty_value = uncertainty_value
        self.node_type = 'BOCUncertainty'
        
        # Create UncertaintyValue object if we have both value and uncertainty
        if value is not None and uncertainty_range is not None:
            self.uncertainty_value = UncertaintyValue(
                value=float(value),
                uncertainty=float(uncertainty_range),
                uncertainty_type=UncertaintyType.ABSOLUTE
            )
    
    def get_absolute_uncertainty(self):
        """Get absolute uncertainty."""
        if self.uncertainty_value:
            return self.uncertainty_value.get_absolute_uncertainty()
        return self.uncertainty_range
    
    def get_relative_uncertainty(self):
        """Get relative uncertainty."""
        if self.uncertainty_value:
            return self.uncertainty_value.get_relative_uncertainty()
        if self.value != 0:
            return self.uncertainty_range / abs(self.value)
        return 0.0
    
    def propagate_add(self, other_uncertainty):
        """Propagate uncertainty through addition."""
        if self.uncertainty_value and other_uncertainty.uncertainty_value:
            result = UncertaintyPropagator.add(self.uncertainty_value, other_uncertainty.uncertainty_value)
            return BOCUncertainty(result.value, result.get_absolute_uncertainty(), result)
        return BOCUncertainty(None, self.uncertainty_range + other_uncertainty.uncertainty_range)
    
    def propagate_multiply(self, other_uncertainty):
        """Propagate uncertainty through multiplication."""
        if self.uncertainty_value and other_uncertainty.uncertainty_value:
            result = UncertaintyPropagator.multiply(self.uncertainty_value, other_uncertainty.uncertainty_value)
            return BOCUncertainty(result.value, result.get_absolute_uncertainty(), result)
        return BOCUncertainty(None, max(self.uncertainty_range, other_uncertainty.uncertainty_range))


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
        elif token_type == BOCTokenType.UPDATE_BELIEF:
            return self.parse_update_belief()
        elif token_type == BOCTokenType.CONFIDENCE_DECAY:
            return self.parse_confidence_decay()
        elif token_type == BOCTokenType.AGENT_COORDINATION:
            return self.parse_agent_coordination()
        elif token_type == BOCTokenType.PROVENANCE:
            return self.parse_provenance()
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
        
        # Enhanced parsing for uncertainty calculations
        result = {
            'type': 'CalculateWithUncertainty', 
            'attributes': attributes, 
            'content': content,
            'uncertainty_analysis': {}
        }
        
        # Extract formula and input uncertainties from content
        formula = None
        input_uncertainties = {}
        
        for item in content:
            if isinstance(item, dict) and item.get('key') == 'formula':
                formula = item.get('value')
            elif isinstance(item, dict) and item.get('key') == 'input_uncertainties':
                # Parse uncertainty values
                uncertainty_obj = item.get('value', {})
                if isinstance(uncertainty_obj, dict) and 'properties' in uncertainty_obj:
                    for var_name, var_uncertainty in uncertainty_obj['properties'].items():
                        if isinstance(var_uncertainty, str) and '±' in var_uncertainty:
                            parsed_unc = self._parse_uncertainty_string(var_uncertainty)
                            input_uncertainties[var_name] = parsed_unc
        
        if formula and input_uncertainties:
            result['uncertainty_analysis'] = {
                'formula': formula,
                'input_uncertainties': input_uncertainties,
                'propagation_possible': True
            }
        
        return result
    
    def _parse_uncertainty_string(self, uncertainty_str):
        """Parse uncertainty string like '±0.1' into UncertaintyValue."""
        if uncertainty_str.startswith('±'):
            uncertainty_value = float(uncertainty_str[1:].strip())
            return {
                'type': 'UncertaintyValue',
                'absolute_uncertainty': uncertainty_value,
                'relative_uncertainty': None  # Will be calculated when base value known
            }
        return None
    
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
    
    def parse_update_belief(self):
        """Parse belief update statement."""
        self.eat(BOCTokenType.UPDATE_BELIEF)
        
        # Parse belief name
        belief_name = self.current_token.value
        self.eat(BOCTokenType.IDENTIFIER)
        
        self.eat(BOCTokenType.LPAREN)
        new_confidence = self.parse_expression()
        self.eat(BOCTokenType.RPAREN)
        
        # Parse evidence source
        evidence_source = None
        if self.current_token.type == BOCTokenType.IDENTIFIER and self.current_token.value == 'evidence':
            self.eat(BOCTokenType.IDENTIFIER)
            self.eat(BOCTokenType.COLON)
            evidence_source = self.parse_expression()
        
        return BOCUpdateBelief(belief_name, new_confidence, evidence_source)
    
    def parse_confidence_decay(self):
        """Parse confidence decay statement."""
        self.eat(BOCTokenType.CONFIDENCE_DECAY)
        
        # Parse belief name
        belief_name = self.current_token.value
        self.eat(BOCTokenType.IDENTIFIER)
        
        self.eat(BOCTokenType.LPAREN)
        decay_function = self.parse_expression()
        self.eat(BOCTokenType.RPAREN)
        
        # Parse time period
        time_period = None
        if self.current_token.type == BOCTokenType.IDENTIFIER and self.current_token.value == 'period':
            self.eat(BOCTokenType.IDENTIFIER)
            self.eat(BOCTokenType.COLON)
            time_period = self.parse_expression()
        
        return BOCConfidenceDecay(belief_name, decay_function, time_period)
    
    def parse_agent_coordination(self):
        """Parse agent coordination statement."""
        self.eat(BOCTokenType.AGENT_COORDINATION)
        
        # Parse coordinator
        coordinator = None
        if self.current_token.type == BOCTokenType.IDENTIFIER and self.current_token.value == 'coordinator':
            self.eat(BOCTokenType.IDENTIFIER)
            self.eat(BOCTokenType.COLON)
            coordinator = self.parse_expression()
        
        content = self.parse_block_content()
        
        # Extract participants and constraints from content
        participants = []
        coordination_type = None
        constraints = []
        
        for item in content:
            if isinstance(item, dict) and item.get('key') == 'participants':
                participants = item.get('value', {}).get('items', [])
            elif isinstance(item, dict) and item.get('key') == 'type':
                coordination_type = item.get('value')
            elif isinstance(item, dict) and item.get('key') == 'constraints':
                constraints = item.get('value', {}).get('items', [])
        
        return BOCAgentCoordination(coordinator, participants, coordination_type, constraints)
    
    def parse_provenance(self):
        """Parse provenance statement."""
        self.eat(BOCTokenType.PROVENANCE)
        
        content = self.parse_block_content()
        
        # Extract source, timestamp, and chain of custody
        source = None
        timestamp = None
        chain_of_custody = []
        
        for item in content:
            if isinstance(item, dict) and item.get('key') == 'source':
                source = item.get('value')
            elif isinstance(item, dict) and item.get('key') == 'timestamp':
                timestamp = item.get('value')
            elif isinstance(item, dict) and item.get('key') == 'chain_of_custody':
                chain_of_custody = item.get('value', {}).get('items', [])
        
        return BOCProvenance(source, timestamp, chain_of_custody)
    
    def parse_assignment(self):
        """Parse a simple assignment."""
        key = self.current_token.value
        self.eat(BOCTokenType.IDENTIFIER)
        self.eat(BOCTokenType.ASSIGN)
        value = self.parse_expression()
        return {'type': 'Assignment', 'key': key, 'value': value}
    
    def parse_expression(self):
        """Parse an expression with uncertainty support."""
        # Handle array expressions first
        if self.current_token.type == BOCTokenType.LBRACKET:
            return self.parse_array()
        
        # Handle uncertainty expressions
        if self.current_token.type == BOCTokenType.UNCERTAINTY:
            return self.parse_uncertainty_expression()
        
        # Handle entity expressions
        if self.current_token.type == BOCTokenType.ENTITY:
            return self.parse_entity_expression()
        
        # Handle object expressions (for nested structures)
        if self.current_token.type == BOCTokenType.LBRACE:
            return self.parse_object_expression()
        
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
    
    def parse_entity_expression(self):
        """Parse entity expressions like entity("name", {...})"""
        self.eat(BOCTokenType.ENTITY)
        
        self.eat(BOCTokenType.LPAREN)
        entity_name = self.parse_expression()
        self.eat(BOCTokenType.COMMA)
        
        # Parse entity properties
        properties = self.parse_object_expression()
        
        self.eat(BOCTokenType.RPAREN)
        
        return {
            'type': 'Entity',
            'name': entity_name,
            'properties': properties
        }
    
    def parse_object_expression(self):
        """Parse object expressions like {key: value, ...}"""
        self.eat(BOCTokenType.LBRACE)
        
        properties = {}
        
        while self.current_token.type != BOCTokenType.RBRACE:
            # Parse key
            if self.current_token.type == BOCTokenType.IDENTIFIER:
                key = self.current_token.value
                self.eat(BOCTokenType.IDENTIFIER)
            elif self.current_token.type == BOCTokenType.STRING:
                key = self.current_token.value
                self.eat(BOCTokenType.STRING)
            else:
                raise Exception(f"Expected identifier or string as object key, got {self.current_token.type.name}")
            
            self.eat(BOCTokenType.COLON)
            
            # Parse value
            value = self.parse_expression()
            properties[key] = value
            
            # Check for comma
            if self.current_token.type == BOCTokenType.COMMA:
                self.eat(BOCTokenType.COMMA)
            elif self.current_token.type != BOCTokenType.RBRACE:
                raise Exception(f"Expected comma or closing brace, got {self.current_token.type.name}")
        
        self.eat(BOCTokenType.RBRACE)
        
        return {
            'type': 'Object',
            'properties': properties
        }
    
    def parse_uncertainty_expression(self):
        """Parse uncertainty expressions like 22.5 ± 0.1"""
        # This method should only be called when we encounter UNCERTAINTY token directly
        # But we need to handle the case where uncertainty follows a number
        
        # If we're called directly on uncertainty, we need to check the previous token context
        # For now, let's return a representation that can be handled
        uncertainty_value = self.current_token.value
        self.eat(BOCTokenType.UNCERTAINTY)
        
        # Extract numeric part from uncertainty (remove ±)
        if uncertainty_value.startswith('±'):
            uncertainty_numeric = uncertainty_value[1:]
        else:
            uncertainty_numeric = uncertainty_value
        
        return BOCUncertainty(None, float(uncertainty_numeric))  # Base value will be set in context
    
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