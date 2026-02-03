#!/usr/bin/env python3
"""
Comprehensive test of the Bot-Optimized Clarity (BOC) language concepts.
"""

from boc_parser import parse_boc_code
import json

def test_comprehensive_boc():
    """Test comprehensive BOC language features."""
    
    comprehensive_boc_code = """
    @timestamp("2026-02-02T19:00:00Z") structured_knowledge {
        entities: [
            entity("temperature_sensor_123", {
                location: "server_room",
                current_reading: 22.5,
                units: "celsius",
                confidence: 0.98
            }),
            entity("power_meter_456", {
                current_draw: 12.4,
                units: "amps",
                status: "nominal"
            })
        ]
    }

    belief confidence=0.85 {
        fact: "temperature_in_celsius(22.5)"
        source: "sensor_123"
        time: "2026-02-02T19:00:00Z"
        certainty_decay: "linear(0.01/hour)"
    }

    reasoning_context {
        assumption: "weather_is_clear"
        evaluate_implications: [
            "temperature_will_rise",
            "solar_power_generation_high"
        ]
        confidence_threshold: 0.7
    }

    intent to_perform: "coordinate_server_room_cooling" {
        target_temperature: 22.0
        acceptable_range: 20.0 .. 24.0
        urgency: "medium"
        deadline: "2026-02-02T20:00:00Z"
    }

    self_capability {
        function: "analyze_sentiment"
        accuracy: 0.87
        training_date: "2026-01-15"
        applicable_to: ["english_text", "social_media"]
        confidence_bounds: [0.7, 0.95]
    }

    calculate_with_uncertainty {
        formula: "demand_forecast = base_demand * seasonality_factor * growth_rate"
        input_uncertainties: {
            base_demand: ±0.1,
            seasonality_factor: ±0.15,
            growth_rate: ±0.05
        }
        output_confidence: "derived_from_inputs"
    }
    """
    
    print("Comprehensive BOC Test Code:")
    print(comprehensive_boc_code)
    print("\nParsing...")
    
    try:
        ast = parse_boc_code(comprehensive_boc_code)
        print("\nParsed successfully!")
        print("The bot-optimized language successfully parses knowledge representations,")
        print("beliefs with confidence levels, reasoning contexts, intents with deadlines,")
        print("self-capabilities, and uncertainty calculations.")
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
    success = test_comprehensive_boc()
    describe_evolution()
    
    if success:
        print("\n✓ Bot-Optimized Clarity (BOC) successfully demonstrates the evolution")
        print("  of the language concept toward a bot-first design philosophy.")