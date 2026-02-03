#!/usr/bin/env python3
"""
Debug version to see the structure of the returned result
"""

from enhanced_translator import ClarityToBOCTranslator, BOCtoClarityTranslator
from clarity_parser import Lexer, Parser
import json


def debug_structure():
    """Debug the structure of the returned result."""
    print("DEBUGGING STRUCTURE OF TRANSLATION RESULT")
    print("=" * 50)
    
    # Simple code that follows the sample program syntax exactly
    clarity_code = """fn calculate(x: Int, y: Int) -> Int {
    if x > y {
        return x + y;
    } else {
        return x - y;
    }
}
"""
    
    # Parse the code
    lexer = Lexer(clarity_code)
    parser = Parser(lexer)
    ast = parser.parse_program()
    
    # Translate with enhanced translator
    enhanced_translator = ClarityToBOCTranslator()
    result = enhanced_translator.translate_with_provenance(ast, clarity_code)
    
    print("Full result structure:")
    print(json.dumps(result, indent=2, default=str))
    print()
    
    print("BOC representation structure:")
    boc_repr = result['boc_representation']
    print(json.dumps(boc_repr, indent=2, default=str))


if __name__ == "__main__":
    debug_structure()