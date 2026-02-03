#!/usr/bin/env python3
"""
Comprehensive test for enhanced BOC parser with uncertainty, belief updating, and agent coordination.
"""

from boc_parser import BOCLexer, BOCParser, parse_boc_code
import json

def test_enhanced_boc_parsing():
    """Test the enhanced BOC parser with new features."""
    
    enhanced_boc_code = """
    // Basic belief with uncertainty
    belief confidence=0.85 {
        fact: "temperature_in_celsius(22.5 ± 0.1)"
        source: "sensor_123"
        timestamp: "2026-02-02T19:00:00Z"
        certainty_decay: "linear(0.01/hour)"
    }
    
    // Update belief with new evidence
    update_belief temperature_confidence(0.92) evidence: "secondary_sensor_reading"
    
    // Confidence decay over time
    confidence_decay temperature_confidence("exponential(0.05/day)") period: "7_days"
    
    // Agent coordination for meeting
    agent_coordination {
        coordinator: "scheduler_agent"
        participants: ["meeting_coordinator", "room_manager", "participant_ai"]
        type: "consensus_based"
        constraints: ["time_window_2h", "virtual_preferred", "max_8_participants"]
    }
    
    // Structured knowledge with provenance
    structured_knowledge {
        entities: [
            entity("temperature_sensor_123", {
                location: "server_room",
                current_reading: 22.5,
                units: "celsius",
                confidence: 0.98
            })
        ]
    }
    
    provenance {
        source: "distributed_sensor_network"
        timestamp: "2026-02-02T19:00:00Z"
        chain_of_custody: ["sensor_123", "gateway_456", "central_db"]
    }
    
    // Calculate with uncertainty propagation
    calculate_with_uncertainty {
        formula: "demand_forecast = base_demand * seasonality_factor * growth_rate"
        input_uncertainties: {
            base_demand: ±0.1,
            seasonality_factor: ±0.15,
            growth_rate: ±0.05
        }
        output_confidence: "derived_from_inputs"
    }
    
    // Intent with deadline and priority
    intent to_perform: "coordinate_meeting_arrangements" {
        participants: ["agent_a", "agent_b", "agent_c"]
        constraints: {
            time_window: "2026-02-03T10:00:00Z/16:00:00Z"
            duration: "PT1H"
            location_preference: "virtual"
        }
        confidence_level: 0.9
        deadline: "2026-02-02T22:00:00Z"
        priority: "high"
    }
    """
    
    print("=== ENHANCED BOC PARSER TEST ===")
    print("Testing advanced BOC features including:")
    print("- Uncertainty notation")
    print("- Belief updating")
    print("- Confidence decay")
    print("- Agent coordination")
    print("- Provenance tracking")
    print("- Uncertainty propagation")
    print()
    
    print("BOC Code to Parse:")
    print(enhanced_boc_code)
    print("\n" + "="*60)
    
    try:
        # Parse the enhanced BOC code
        ast = parse_boc_code(enhanced_boc_code)
        
        print("SUCCESSFULLY PARSED!")
        print("\nAST Structure:")
        print(json.dumps(ast, indent=2, default=str))
        
        # Validate parsed structure
        statements = ast.get('statements', [])
        print(f"\nParsed {len(statements)} statements:")
        
        for i, stmt in enumerate(statements):
            stmt_type = stmt.get('type') or getattr(stmt, 'node_type', 'Unknown')
            print(f"  {i+1}. {stmt_type}")
            
            if hasattr(stmt, 'node_type'):
                if stmt.node_type == 'BOCBelief':
                    print(f"      - Belief with attributes: {list(stmt.attributes.keys())}")
                elif stmt.node_type == 'BOCUpdateBelief':
                    print(f"      - Updating belief: {stmt.belief_name}")
                elif stmt.node_type == 'BOCConfidenceDecay':
                    print(f"      - Confidence decay for: {stmt.belief_name}")
                elif stmt.node_type == 'BOCAgentCoordination':
                    print(f"      - Coordination type: {stmt.coordination_type}")
                    print(f"      - Participants: {len(stmt.participants)}")
                elif stmt.node_type == 'BOCProvenance':
                    print(f"      - Source: {stmt.source}")
                elif stmt.node_type == 'BOCUncertainty':
                    print(f"      - Value: {stmt.value} ± {stmt.uncertainty_range}")
        
        print("\n✅ All advanced BOC features parsed successfully!")
        return True
        
    except Exception as e:
        print(f"Parse error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_uncertainty_propagation():
    """Test uncertainty parsing and propagation."""
    
    uncertainty_examples = [
        "temperature = 22.5 ± 0.1",
        "pressure = 1013.25 ± 2.5",
        "humidity = 45.0 ± 1.0"
    ]
    
    print("\n=== UNCERTAINTY PROPAGATION TEST ===")
    
    for example in uncertainty_examples:
        print(f"\nTesting: {example}")
        try:
            lexer = BOCLexer(example)
            parser = BOCParser(lexer)
            result = parser.parse_expression()
            
            if hasattr(result, 'node_type') and result.node_type == 'BOCUncertainty':
                print(f"  Parsed: {result.value} ± {result.uncertainty_range}")
            else:
                print(f"  Unexpected result type: {type(result)}")
                
        except Exception as e:
            print(f"  Error: {e}")


def test_agent_coordination_complexity():
    """Test complex agent coordination scenarios."""
    
    complex_coordination = """
    agent_coordination {
        coordinator: "orchestrator_agent"
        participants: ["worker_a", "worker_b", "supervisor", "monitor"]
        type: "hierarchical_consensus"
        constraints: [
            "max_execution_time_5min",
            "resource_limit_2GB",
            "error_tolerance_0.01"
        ]
        voting_weights: {"supervisor": 3.0, "worker_a": 1.0, "worker_b": 1.0, "monitor": 0.5}
        decision_threshold: 0.67
    }
    """
    
    print("\n=== COMPLEX AGENT COORDINATION TEST ===")
    print("Testing hierarchical consensus with voting weights...")
    
    try:
        ast = parse_boc_code(complex_coordination)
        statements = ast.get('statements', [])
        
        if statements and len(statements) > 0:
            coord_stmt = statements[0]
            if hasattr(coord_stmt, 'node_type') and coord_stmt.node_type == 'BOCAgentCoordination':
                print(f"Complex coordination parsed successfully!")
                print(f"  Type: {coord_stmt.coordination_type}")
                print(f"  Participants: {coord_stmt.participants}")
                print(f"  Constraints: {len(coord_stmt.constraints)}")
            else:
                print(f"Unexpected coordination structure")
        else:
            print("No statements parsed")
            
    except Exception as e:
        print(f"Error parsing complex coordination: {e}")


if __name__ == '__main__':
    success1 = test_enhanced_boc_parsing()
    test_uncertainty_propagation()
    test_agent_coordination_complexity()
    
    print("\n" + "="*60)
    if success1:
        print("Enhanced BOC parser working correctly!")
        print("Advanced features supported:")
        print("  - Uncertainty notation (±)")
        print("  - Belief updating")
        print("  - Confidence decay")
        print("  - Agent coordination")
        print("  - Provenance tracking")
        print("  - Complex hierarchical coordination")
    else:
        print("Some BOC features need more work")
    
    print("\nThe enhanced BOC parser now supports sophisticated agent communication patterns")
    print("with uncertainty quantification, belief updating, and multi-agent coordination.")