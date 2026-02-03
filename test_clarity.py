#!/usr/bin/env python3
"""
Test script for the Clarity language parser.
"""

from clarity_parser import Lexer, Parser, print_ast

def test_basic_parsing():
    print("=== Testing Basic Parsing ===")
    
    # Test 1: Simple variable declarations
    code1 = """
    let x: Int = 42;
    var y = x + 10;
    const MAX = 100;
    """
    
    print("Code 1:")
    print(code1)
    print("\nTokens:")
    lexer = Lexer(code1)
    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type.name == 'EOF':
            break
    
    print("\n" + "="*50)


def test_function_parsing():
    print("=== Testing Function Parsing ===")
    
    code2 = """
    fn add(a: Int, b: Int) -> Int {
        return a + b;
    }
    
    fn main() {
        let result = add(5, 10);
        return result;
    }
    """
    
    print("Code 2:")
    print(code2)
    
    print("\nParsing AST:")
    lexer = Lexer(code2)
    parser = Parser(lexer)
    try:
        ast = parser.parse_program()
        print_ast(ast, 0)
    except Exception as e:
        print(f"Parse error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)


def test_control_flow():
    print("=== Testing Control Flow ===")
    
    code3 = """
    fn factorial(n: Int) -> Int {
        if n <= 1 {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    fn main() {
        let num = 5;
        let result = factorial(num);
        if result > 100 {
            println("Large result!");
        }
        return result;
    }
    """
    
    print("Code 3:")
    print(code3)
    
    print("\nParsing AST:")
    lexer = Lexer(code3)
    parser = Parser(lexer)
    try:
        ast = parser.parse_program()
        # Just print the top-level structure to avoid too much output
        print(f"Program has {len(ast.statements)} top-level statements")
        for i, stmt in enumerate(ast.statements):
            print(f"  Statement {i+1}: {stmt.node_type} - {getattr(stmt, 'name', 'unnamed')}")
    except Exception as e:
        print(f"Parse error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)


def test_expressions():
    print("=== Testing Expression Parsing ===")
    
    expressions = [
        "x + y * z",
        "a && b || c",
        "value == 42",
        "!(x < 10)",
        "func(a, b, c)"
    ]
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        lexer = Lexer(expr)
        parser = Parser(lexer)
        try:
            ast = parser.parse_expression()
            print(f"Parsed as: {ast.node_type}")
        except Exception as e:
            print(f"Parse error: {e}")


if __name__ == "__main__":
    test_basic_parsing()
    test_function_parsing()
    test_control_flow()
    test_expressions()
    
    print("\n=== All tests completed ===")