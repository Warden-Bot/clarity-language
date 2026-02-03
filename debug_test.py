from language_project.clarity_parser import Lexer

# Test simple function
code = 'fn test() { let x = n - 1; }'
print("Testing code:", code)
lexer = Lexer(code)

while True:
    token = lexer.get_next_token()
    print(token)
    if token.type.name == 'EOF':
        break