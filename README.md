# Clarity Language

A dual-layer programming language designed for human-AI collaborative programming.

## Overview

Clarity is a programming language that features a dual-layer architecture:
- **Surface Layer**: Human-readable syntax designed for developers
- **Deep Layer**: Agent-optimized bytecode for AI processing

This approach allows for human-readable code while providing efficient representations for AI agents to work with.

## Features

- Human-readable syntax
- AI-optimized bytecode representation
- Semantic preservation between layers
- Source mapping for debugging across layers
- Version compatibility tracking
- Trust boundary validation

## Architecture

The dual-layer architecture ensures that both humans and AI agents can effectively work with the same codebase:
- Surface layer optimized for human comprehension and modification
- Deep layer optimized for AI analysis and transformation
- Cryptographic proofs ensuring semantic equivalence
- Comprehensive source maps for cross-layer debugging

## Files

- `clarity_parser.py` - Parser for the Clarity surface language
- `boc_parser.py` - Parser for the Bytecode Optimized Clarity (BOC) deep layer
- `translator.py` - Translator between surface and deep layers with provenance tracking
- `clarity_interpreter.py` - Interpreter for Clarity code
- Various `.clar` files - Sample Clarity programs
- Documentation files in Markdown format

## Usage

```python
from clarity_parser import Lexer, Parser
from translator import ClarityToBOCTranslator

# Example usage
code = """
fn calculate(x: Int, y: Int) -> Int {
    if x > y {
        return x + y;
    } else {
        return x - y;
    }
}
"""

lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse_program()

translator = ClarityToBOCTranslator()
result = translator.translate_with_provenance(ast, code)
print(result)
```

## Contributing

See the documentation files for detailed information about contributing to the Clarity language project.

## License

MIT License - see LICENSE file for details.