#!/usr/bin/env python3
"""
Basic interpreter for the Clarity programming language.
This provides runtime execution of parsed Clarity programs.
"""

from clarity_parser import *
import math


class Environment:
    """Manages variable bindings during execution."""
    
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    
    def define(self, name, value):
        self.vars[name] = value
    
    def assign(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"Undefined variable: {name}")
    
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable: {name}")


class Interpreter:
    """Interprets and executes Clarity AST nodes."""
    
    def __init__(self):
        self.global_env = Environment()
        # Pre-populate with built-in functions
        self.global_env.define('println', self._builtin_println)
        self.global_env.define('sqrt', self._builtin_sqrt)
    
    def _builtin_println(self, *args):
        """Built-in println function."""
        print(*args)
        return None
    
    def _builtin_sqrt(self, value):
        """Built-in square root function."""
        return math.sqrt(value)
    
    def visit_Program(self, node):
        """Execute a program (sequence of statements)."""
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result
    
    def visit_FunctionDef(self, node):
        """Define a function in the environment."""
        self.global_env.define(node.name, node)
        return None
    
    def visit_VariableDecl(self, node):
        """Execute a variable declaration."""
        value = self.visit(node.value)
        
        if node.var_type and node.var_type != 'Int' and node.var_type != 'Float' and node.var_type != 'Bool' and node.var_type != 'String':
            # Type checking would happen here in a full implementation
            pass
        
        self.global_env.define(node.name, value)
        return value
    
    def visit_ConstantDecl(self, node):
        """Execute a constant declaration."""
        value = self.visit(node.value)
        self.global_env.define(node.name, value)
        return value
    
    def visit_Assignment(self, node):
        """Execute an assignment."""
        value = self.visit(node.value)
        self.global_env.assign(node.name, value)
        return value
    
    def visit_BinaryOp(self, node):
        """Execute a binary operation."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '&&':
            return left and right
        elif node.operator == '||':
            return left or right
        else:
            raise ValueError(f"Unknown operator: {node.operator}")
    
    def visit_UnaryOp(self, node):
        """Execute a unary operation."""
        operand = self.visit(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator == '!':
            return not operand
        else:
            raise ValueError(f"Unknown unary operator: {node.operator}")
    
    def visit_IfExpr(self, node):
        """Execute an if expression."""
        condition = self.visit(node.condition)
        
        if condition:
            env_before = self.global_env
            self.global_env = Environment(parent=self.global_env)
            try:
                result = None
                for stmt in node.then_branch:
                    result = self.visit(stmt)
                return result
            finally:
                self.global_env = env_before
        elif node.else_branch:
            env_before = self.global_env
            self.global_env = Environment(parent=self.global_env)
            try:
                result = None
                for stmt in node.else_branch:
                    result = self.visit(stmt)
                return result
            finally:
                self.global_env = env_before
        else:
            return None
    
    def visit_WhileLoop(self, node):
        """Execute a while loop."""
        result = None
        while self.visit(node.condition):
            env_before = self.global_env
            self.global_env = Environment(parent=self.global_env)
            try:
                for stmt in node.body:
                    result = self.visit(stmt)
            finally:
                self.global_env = env_before
        return result
    
    def visit_ForLoop(self, node):
        """Execute a for loop (simplified for this demo)."""
        # This is a simplified implementation
        # In a full implementation, we'd need to handle different iterable types
        iterable = self.visit(node.iterable)
        
        if isinstance(iterable, list):
            result = None
            for item in iterable:
                env_before = self.global_env
                self.global_env = Environment(parent=self.global_env)
                try:
                    self.global_env.define(node.variable, item)
                    for stmt in node.body:
                        result = self.visit(stmt)
                finally:
                    self.global_env = env_before
            return result
        else:
            raise TypeError(f"Cannot iterate over {type(iterable)}")
    
    def visit_ReturnStmt(self, node):
        """Execute a return statement."""
        if node.value:
            return self.visit(node.value)
        else:
            return None
    
    def visit_FunctionCall(self, node):
        """Execute a function call."""
        # Get the function definition
        func_def = self.global_env.get(node.name)
        
        if callable(func_def):
            # Built-in function
            arg_values = [self.visit(arg) for arg in node.args]
            return func_def(*arg_values)
        elif isinstance(func_def, FunctionDef):
            # User-defined function
            if len(node.args) != len(func_def.params):
                raise ValueError(f"Function {node.name} expects {len(func_def.params)} arguments but got {len(node.args)}")
            
            # Prepare arguments
            arg_values = [self.visit(arg) for arg in node.args]
            arg_bindings = {param[0]: val for param, val in zip(func_def.params, arg_values)}
            
            # Create new environment with arguments
            old_env = self.global_env
            self.global_env = Environment(parent=old_env)
            for name, value in arg_bindings.items():
                self.global_env.define(name, value)
            
            try:
                result = None
                for stmt in func_def.body:
                    result = self.visit(stmt)
                    # If we encounter a return statement, use its value
                    if isinstance(stmt, ReturnStmt):
                        return result
                return result
            finally:
                self.global_env = old_env
        else:
            raise NameError(f"{node.name} is not callable")
    
    def visit_Identifier(self, node):
        """Evaluate an identifier."""
        return self.global_env.get(node.name)
    
    def visit_Number(self, node):
        """Evaluate a number literal."""
        return node.value
    
    def visit_String(self, node):
        """Evaluate a string literal."""
        return node.value
    
    def visit_Boolean(self, node):
        """Evaluate a boolean literal."""
        return node.value
    
    def visit_MatchExpr(self, node):
        """Execute a match expression."""
        # Simplified implementation - only handles direct value matching
        matched_value = self.visit(node.expr)
        
        for pattern, result_expr in node.arms:
            # In a full implementation, we'd handle pattern matching properly
            # For now, we'll do simple value comparison
            if isinstance(pattern, (Number, String, Boolean)):
                pattern_value = self.visit(pattern)
                if matched_value == pattern_value:
                    return self.visit(result_expr)
            elif isinstance(pattern, Identifier):
                # This would be a catch-all pattern in a real implementation
                return self.visit(result_expr)
        
        raise ValueError(f"No match found for value: {matched_value}")
    
    def visit(self, node):
        """Generic visit method to dispatch to specific visitor methods."""
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Called when no specific visitor method is found."""
        raise Exception(f'No visitor method for {node.node_type}')
    
    def interpret(self, ast):
        """Interpret the given AST."""
        return self.visit(ast)


def run_file(filename):
    """Run a Clarity source file."""
    with open(filename, 'r') as f:
        source = f.read()
    
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse_program()
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    return result


def repl():
    """Simple REPL for interactive execution."""
    print("Clarity Language REPL")
    print("Enter expressions to evaluate, or 'quit' to exit.")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() in ['quit', 'exit', 'q']:
                break
            
            if not line.strip():
                continue
                
            lexer = Lexer(line)
            parser = Parser(lexer)
            ast = parser.parse_expression()
            
            result = interpreter.visit(ast)
            print(result)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run a file
        filename = sys.argv[1]
        print(f"Running {filename}...")
        try:
            result = run_file(filename)
            print(f"Program returned: {result}")
        except Exception as e:
            print(f"Runtime error: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Start REPL
        repl()