from language_project.clarity_parser import Lexer, Parser

# Test the specific problematic code
code = """
fn factorial(n: Int) -> Int {
    return n * factorial(n - 1);
}
"""

print("Testing problematic code:")
print(code)
print("\nTokens:")
lexer = Lexer(code)
tokens = []
while True:
    token = lexer.get_next_token()
    tokens.append(token)
    print(token)
    if token.type.name == 'EOF':
        break

print("\nAttempting to parse:")
lexer = Lexer(code)
parser = Parser(lexer)

try:
    ast = parser.parse_program()
    print("Successfully parsed!")
except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()