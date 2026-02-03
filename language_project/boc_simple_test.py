#!/usr/bin/env python3
"""
Simple test of the Bot-Optimized Clarity (BOC) language concepts.
"""

from boc_parser import parse_boc_code
import json

def test_simple_boc():
    """Test simple BOC language features."""
    
    simple_boc_code = """
    belief confidence=0.85 {
        fact: "temperature_is_22_degrees"
        source: "sensor_123"
        timestamp: "2026-02-02T19:00:00Z"
    }

    reasoning_context {
        assumption: "weather_is_clear"
        confidence_threshold: 0.7
    }

    intent to_perform: "adjust_temperature" {
        target: 22.0
        urgency: "low"
        deadline: "2026-02-02T20:00:00Z"
    }

    self_capability {
        function: "analyze_sentiment"
        accuracy: 0.87
    }
    """
    
    print("Simple BOC Test Code:")
    print(simple_boc_code)
    print("\nParsing...")
    
    try:
        ast = parse_boc_code(simple_boc_code)
        print("\n✓ Parsed successfully!")
        print("\nThe bot-optimized language successfully demonstrates:")
        print("- BELIEF statements with confidence levels")
        print("- REASONING_CONTEXT for logical inference") 
        print("- INTENT declarations for multi-agent coordination")
        print("- SELF_CAPABILITY introspection")
        return True
    except Exception as e:
        print(f"\nParse error: {e}")
        import traceback
        traceback.print_exc()
        return False


def describe_evolution():
    """Describe the evolution from human-focused to bot-focused language."""
    
    print("\n" + "="*70)
    print("EVOLUTION FROM CLARITY TO BOT-OPTIMIZED CLARITY (BOC)")
    print("="*70)
    
    print("""
Original Clarity (Human-Focused):
---------------------------------
• Readable syntax resembling Python/Rust
• Traditional programming constructs
• Error messages optimized for humans
• General-purpose computational tasks

Bot-Optimized Clarity (BOC):
----------------------------
• Knowledge representation primitives
• Confidence and uncertainty modeling
• Belief systems with sources and decay
• Reasoning and inference constructs  
• Self-awareness and capability modeling
• Communication-first design
• Rich metadata and provenance tracking
• Collaborative state management

Key Innovations in BOC:
-----------------------
1. BELIEF statements with confidence levels
2. REASONING_CONTEXT for logical inference
3. INTENT declarations for multi-agent coordination
4. SELF_CAPABILITY introspection
5. UNCERTAINTY propagation in calculations
6. STRUCTURED_KNOWLEDGE with rich metadata
7. Built-in provenance and source tracking

This represents a fundamental shift from a language for computation
to a language for knowledge exchange, reasoning, and collaboration
between AI agents.
""")


if __name__ == "__main__":
    success = test_simple_boc()
    describe_evolution()
    
    if success:
        print("\n✓ Bot-Optimized Clarity (BOC) successfully demonstrates the evolution")
        print("  of the language concept toward a bot-first design philosophy.")