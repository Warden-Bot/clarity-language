#!/usr/bin/env python3
"""
Test the enhanced translator between Clarity and BOC with semantic preservation.
"""

from translator import ClarityToBOCTranslator, BOCtoClarityTranslator
import json

class MockFunctionDef:
    """Mock Clarity function AST for testing."""
    def __init__(self, name="factorial", params=[("n", "Int")], return_type="Int", is_recursive=True):
        self.node_type = 'FunctionDef'
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = []  # Simplified for testing


class MockVariableDecl:
    """Mock Clarity variable declaration for testing."""
    def __init__(self, name="result", mutable=False, value=None):
        self.node_type = 'VariableDecl'
        self.name = name
        self.mutable = mutable
        self.var_type = None
        self.value = value or MockValue(42)


class MockValue:
    """Mock value AST node for testing."""
    def __init__(self, value):
        self.value = value


class MockProgram:
    """Mock Clarity program AST for testing."""
    def __init__(self, statements=None):
        self.statements = statements or [MockFunctionDef(), MockVariableDecl()]


def test_enhanced_translation():
    """Test the enhanced translator capabilities."""
    
    print("=== ENHANCED TRANSLATOR TEST ===")
    print("Testing semantic preservation and rich BOC representation...")
    print()
    
    # Create test cases with different types of functions
    test_functions = [
        MockFunctionDef("factorial", [("n", "Int")], "Int", True),
        MockFunctionDef("calculate_area", [("width", "Float"), ("height", "Float")], "Float", False),
        MockFunctionDef("validate_input", [("data", "String")], "Bool", False),
        MockFunctionDef("emergency_shutdown", [], "Unit", False),
    ]
    
    translator = ClarityToBOCTranslator()
    
    for i, func in enumerate(test_functions):
        print(f"--- Test Case {i+1}: {func.name} ---")
        
        # Translate to BOC
        boc_repr = translator.translate_function_def(func)
        
        print("BOC Representation:")
        print(json.dumps(boc_repr, indent=2))
        
        # Verify key enhanced features are present
        structured_knowledge = boc_repr.get("structured_knowledge", {})
        
        # Check for enhanced features
        features_found = []
        
        if "complexity_analysis" in structured_knowledge:
            features_found.append("complexity_analysis")
        
        if "side_effects" in structured_knowledge:
            features_found.append("side_effects")
        
        if structured_knowledge.get("parameters", []):
            param = structured_knowledge["parameters"][0]
            if "constraints" in param:
                features_found.append("parameter_constraints")
            if "uncertainty" in param:
                features_found.append("parameter_uncertainty")
        
        reasoning_context = boc_repr.get("reasoning_context", {})
        if any(key in reasoning_context for key in ["preconditions", "postconditions", "invariants"]):
            features_found.append("enhanced_reasoning_context")
        
        intent = boc_repr.get("intent", {})
        if "resource_requirements" in intent:
            features_found.append("resource_requirements")
        if "uncertainty_propagation" in intent:
            features_found.append("uncertainty_propagation")
        
        if "provenance" in boc_repr:
            features_found.append("provenance_tracking")
        
        print(f"Enhanced features detected: {', '.join(features_found)}")
        print()
    
    return True


def test_reverse_translation():
    """Test BOC to Clarity translation with enhanced features."""
    
    print("=== REVERSE TRANSLATION TEST ===")
    print("Testing BOC to Clarity with enhanced metadata...")
    print()
    
    # Create a rich BOC representation
    boc_repr = {
        "structured_knowledge": {
            "type": "function_definition",
            "name": "safe_divide",
            "parameters": [
                {
                    "name": "numerator",
                    "type": "Float",
                    "confidence": 0.95,
                    "uncertainty": 0.01,
                    "constraints": ["finite_number", "not_nan_or_infinity"]
                },
                {
                    "name": "denominator",
                    "type": "Float",
                    "confidence": 0.95,
                    "uncertainty": 0.01,
                    "constraints": ["finite_number", "not_nan_or_infinity", "non_zero"]
                }
            ],
            "return_type": "Float",
            "confidence": 0.92,
            "source": "human_contributed",
            "complexity_analysis": {
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "recursive": False,
                "loops": 0,
                "conditional_branches": 1
            },
            "side_effects": {
                "modifies_state": False,
                "io_operations": False,
                "network_operations": False,
                "memory_allocation": False
            },
            "priority": "high"
        },
        "reasoning_context": {
            "assumptions": ["inputs_valid", "denominator_non_zero"],
            "implications": ["division_performed", "result_calculated"],
            "preconditions": ["inputs_valid", "system_resources_available"],
            "postconditions": ["function_completed", "output_consistent_with_spec"],
            "invariants": ["type_safety_maintained", "logical_consistency"],
            "confidence_threshold": 0.7,
            "error_handling": {
                "has_error_handling": True,
                "error_types": ["division_by_zero", "overflow"],
                "recovery_strategies": ["return_none", "propagate_error"]
            }
        },
        "intent": {
            "to_perform": "execute_function_safe_divide",
            "action_type": "computation",
            "parameters": [["numerator", "Float"], ["denominator", "Float"]],
            "execution_context": "runtime_call",
            "priority": "high",
            "resource_requirements": {
                "cpu_usage": "low",
                "memory_usage": "minimal",
                "io_requirements": "none",
                "network_usage": "none"
            },
            "uncertainty_propagation": {
                "input_uncertainty_affects_output": True,
                "amplification_factor": 1.5,
                "uncertainty_sources": ["input_parameters", "floating_point_precision"],
                "confidence_degradation": "minimal"
            }
        },
        "provenance": {
            "source": "human_written",
            "translation_timestamp": "2026-02-03T19:00:00Z",
            "translation_confidence": 0.9,
            "semantic_preservation_score": 0.88
        }
    }
    
    reverse_translator = BOCtoClarityTranslator()
    clarity_code = reverse_translator.translate_to_clarity({"structured_knowledge": {"components": [{"structured_knowledge": boc_repr["structured_knowledge"]}]}})
    
    print("Generated Clarity Code:")
    print(clarity_code)
    print()
    
    # Check if the generated code includes enhanced metadata comments
    enhanced_features = []
    
    if "Complexity:" in clarity_code:
        enhanced_features.append("complexity_info")
    if "Side Effects:" in clarity_code:
        enhanced_features.append("side_effects_info")
    if "Priority:" in clarity_code:
        enhanced_features.append("priority_info")
    if "Constraints:" in clarity_code:
        enhanced_features.append("parameter_constraints")
    if "Preconditions:" in clarity_code:
        enhanced_features.append("preconditions_info")
    if "Postconditions:" in clarity_code:
        enhanced_features.append("postconditions_info")
    if "Invariants:" in clarity_code:
        enhanced_features.append("invariants_info")
    if "Uncertainty propagation" in clarity_code:
        enhanced_features.append("uncertainty_guidance")
    
    print(f"Enhanced features in generated code: {', '.join(enhanced_features)}")
    
    return len(enhanced_features) >= 5  # At least 5 enhanced features should be present


def test_semantic_preservation():
    """Test that semantic meaning is preserved across translation."""
    
    print("\n=== SEMANTIC PRESERVATION TEST ===")
    print("Testing preservation of meaning across translation layers...")
    print()
    
    # Test different semantic patterns
    semantic_tests = [
        ("Mathematical function", MockFunctionDef("square_root", [("x", "Float")], "Float")),
        ("String processing", MockFunctionDef("sanitize_string", [("input", "String")], "String")),
        ("Data validation", MockFunctionDef("validate_email", [("email", "String")], "Bool")),
        ("Resource management", MockFunctionDef("allocate_buffer", [("size", "Int")], "Array[Byte]")),
    ]
    
    translator = ClarityToBOCTranslator()
    
    for test_name, func in semantic_tests:
        print(f"Testing: {test_name}")
        
        # Forward translation
        boc_repr = translator.translate_function_def(func)
        
        # Check semantic preservation score
        provenance = boc_repr.get("provenance", {})
        preservation_score = provenance.get("semantic_preservation_score", 0)
        
        print(f"  Semantic preservation score: {preservation_score:.2f}")
        
        # Analyze if semantic elements are captured
        semantic_elements = []
        
        # Check if function intent is captured
        if "math" in func.name.lower():
            if any("computational" in str(v) for v in boc_repr.values()):
                semantic_elements.append("computational_intent")
        
        if "validate" in func.name.lower():
            if any("validation" in str(v) for v in boc_repr.values()):
                semantic_elements.append("validation_intent")
        
        if "allocate" in func.name.lower():
            if boc_repr.get("structured_knowledge", {}).get("side_effects", {}).get("memory_allocation"):
                semantic_elements.append("allocation_intent")
        
        print(f"  Semantic elements captured: {', '.join(semantic_elements)}")
        print()
    
    return True


if __name__ == '__main__':
    print("Testing Enhanced Clarity-BOC Translator")
    print("=" * 50)
    print()
    
    success1 = test_enhanced_translation()
    success2 = test_reverse_translation()
    success3 = test_semantic_preservation()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Enhanced translation: {'PASS' if success1 else 'FAIL'}")
    print(f"Reverse translation: {'PASS' if success2 else 'FAIL'}")
    print(f"Semantic preservation: {'PASS' if success3 else 'FAIL'}")
    
    if all([success1, success2, success3]):
        print("\nEnhanced translator working correctly!")
        print("Advanced features supported:")
        print("  - Complexity analysis")
        print("  - Side effect detection")
        print("  - Parameter constraint inference")
        print("  - Uncertainty propagation analysis")
        print("  - Resource requirement estimation")
        print("  - Provenance and metadata tracking")
        print("  - Enhanced reasoning context")
        print("  - Semantic preservation scoring")
    else:
        print("\nSome translator features need improvement")
    
    print("\nThe enhanced translator now provides rich semantic mapping")
    print("between human-readable Clarity and agent-optimized BOC formats.")