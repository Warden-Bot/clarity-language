#!/usr/bin/env python3
"""
Belief management system for BOC - handles belief updating and confidence decay over time.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import math


class DecayFunction(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    STEP = "step"
    CUSTOM = "custom"


class EvidenceType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CONTRADICTORY = "contradictory"


@dataclass
class Evidence:
    """Represents evidence for or against a belief."""
    content: str
    confidence: float
    source: str
    timestamp: datetime
    evidence_type: EvidenceType
    weight: float = 1.0


@dataclass
class BeliefState:
    """Represents the current state of a belief."""
    name: str
    initial_confidence: float
    current_confidence: float
    created_at: datetime
    last_updated: datetime
    decay_function: DecayFunction
    decay_rate: float
    decay_period: timedelta
    evidence_history: List[Evidence] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    min_confidence: float = 0.0
    max_confidence: float = 1.0
    active: bool = True
    
    def age_in_seconds(self) -> float:
        """Get the age of the belief in seconds."""
        return (datetime.now() - self.last_updated).total_seconds()
    
    def age_in_periods(self) -> float:
        """Get the age of the belief in decay periods."""
        return self.age_in_seconds() / self.decay_period.total_seconds()


class BeliefManager:
    """Manages belief states, updates, and confidence decay."""
    
    def __init__(self):
        self.beliefs: Dict[str, BeliefState] = {}
        self.decay_functions: Dict[DecayFunction, Callable] = {
            DecayFunction.LINEAR: self._linear_decay,
            DecayFunction.EXPONENTIAL: self._exponential_decay,
            DecayFunction.LOGARITHMIC: self._logarithmic_decay,
            DecayFunction.STEP: self._step_decay,
            DecayFunction.CUSTOM: self._custom_decay
        }
    
    def create_belief(self, 
                      name: str, 
                      initial_confidence: float,
                      decay_function: DecayFunction = DecayFunction.EXPONENTIAL,
                      decay_rate: float = 0.1,
                      decay_period: timedelta = timedelta(hours=1),
                      metadata: Dict = None) -> BeliefState:
        """Create a new belief state."""
        
        if not 0.0 <= initial_confidence <= 1.0:
            raise ValueError("Initial confidence must be between 0.0 and 1.0")
        
        now = datetime.now()
        belief = BeliefState(
            name=name,
            initial_confidence=initial_confidence,
            current_confidence=initial_confidence,
            created_at=now,
            last_updated=now,
            decay_function=decay_function,
            decay_rate=decay_rate,
            decay_period=decay_period,
            metadata=metadata or {}
        )
        
        self.beliefs[name] = belief
        return belief
    
    def update_belief(self, 
                      name: str, 
                      new_confidence: float,
                      evidence: Optional[Evidence] = None) -> bool:
        """Update a belief with new confidence and optional evidence."""
        
        if name not in self.beliefs:
            return False
        
        belief = self.beliefs[name]
        
        if not 0.0 <= new_confidence <= 1.0:
            raise ValueError("New confidence must be between 0.0 and 1.0")
        
        # Apply confidence decay first
        decayed_confidence = self.apply_decay(belief)
        
        # Combine decayed confidence with new evidence
        if evidence:
            belief.evidence_history.append(evidence)
            # Weight evidence by its confidence and recency
            evidence_weight = self._calculate_evidence_weight(evidence, belief)
            combined_confidence = self._combine_confidences(
                decayed_confidence, new_confidence, evidence_weight
            )
        else:
            combined_confidence = new_confidence
        
        belief.current_confidence = max(belief.min_confidence, 
                                       min(belief.max_confidence, combined_confidence))
        belief.last_updated = datetime.now()
        
        return True
    
    def apply_decay(self, belief: BeliefState) -> float:
        """Apply confidence decay to a belief."""
        if not belief.active:
            return belief.current_confidence
        
        age_periods = belief.age_in_periods()
        decay_func = self.decay_functions.get(belief.decay_function)
        
        if decay_func:
            decayed_confidence = decay_func(belief.current_confidence, 
                                          belief.decay_rate, age_periods)
            return max(belief.min_confidence, 
                      min(belief.max_confidence, decayed_confidence))
        
        return belief.current_confidence
    
    def get_current_confidence(self, name: str) -> Optional[float]:
        """Get the current confidence of a belief (with decay applied)."""
        if name not in self.beliefs:
            return None
        
        belief = self.beliefs[name]
        return self.apply_decay(belief)
    
    def get_all_beliefs(self, apply_decay: bool = True) -> Dict[str, BeliefState]:
        """Get all belief states, optionally applying decay."""
        if apply_decay:
            # Create a copy with decay applied
            result = {}
            for name, belief in self.beliefs.items():
                # Update temporary confidence without modifying the original
                temp_belief = BeliefState(**belief.__dict__)
                temp_belief.current_confidence = self.apply_decay(belief)
                result[name] = temp_belief
            return result
        else:
            return self.beliefs.copy()
    
    def _linear_decay(self, confidence: float, decay_rate: float, age_periods: float) -> float:
        """Linear decay: C(t) = C0 - r*t"""
        return max(0.0, confidence - decay_rate * age_periods)
    
    def _exponential_decay(self, confidence: float, decay_rate: float, age_periods: float) -> float:
        """Exponential decay: C(t) = C0 * e^(-r*t)"""
        return confidence * math.exp(-decay_rate * age_periods)
    
    def _logarithmic_decay(self, confidence: float, decay_rate: float, age_periods: float) -> float:
        """Logarithmic decay: C(t) = C0 / (1 + r*log(1 + t))"""
        return confidence / (1 + decay_rate * math.log(1 + age_periods))
    
    def _step_decay(self, confidence: float, decay_rate: float, age_periods: float) -> float:
        """Step decay: C(t) = C0 * r^floor(t)"""
        steps = math.floor(age_periods)
        return confidence * (decay_rate ** steps)
    
    def _custom_decay(self, confidence: float, decay_rate: float, age_periods: float) -> float:
        """Custom decay function (placeholder for user-defined)."""
        # Default to exponential if no custom function provided
        return self._exponential_decay(confidence, decay_rate, age_periods)
    
    def _calculate_evidence_weight(self, evidence: Evidence, belief: BeliefState) -> float:
        """Calculate the weight of evidence based on recency and type."""
        recency_factor = 1.0
        age_hours = (datetime.now() - evidence.timestamp).total_seconds() / 3600
        
        # More recent evidence has higher weight
        if age_hours < 1:
            recency_factor = 1.0
        elif age_hours < 24:
            recency_factor = 0.8
        elif age_hours < 168:  # 1 week
            recency_factor = 0.6
        else:
            recency_factor = 0.4
        
        # Evidence type affects weight
        type_factor = {
            EvidenceType.POSITIVE: 1.2,
            EvidenceType.NEGATIVE: 1.1,
            EvidenceType.NEUTRAL: 0.8,
            EvidenceType.CONTRADICTORY: 0.5
        }.get(evidence.evidence_type, 1.0)
        
        return evidence.weight * recency_factor * type_factor
    
    def _combine_confidences(self, 
                           current_confidence: float, 
                           new_confidence: float, 
                           evidence_weight: float) -> float:
        """Combine current confidence with new evidence."""
        # Weighted average with evidence weight
        if evidence_weight > 1.0:
            # Strong evidence shifts confidence more
            weight = evidence_weight / (evidence_weight + 1.0)
        else:
            # Normal weighted average
            weight = 0.5
        
        return (1 - weight) * current_confidence + weight * new_confidence
    
    def add_contradictory_evidence(self, belief_name: str, evidence: Evidence) -> float:
        """Add contradictory evidence and calculate conflict penalty."""
        if belief_name not in self.beliefs:
            return 0.0
        
        belief = self.beliefs[belief_name]
        belief.evidence_history.append(evidence)
        
        # Calculate conflict penalty
        conflict_penalty = evidence.confidence * 0.3  # Reduce confidence by 30% of evidence confidence
        belief.current_confidence = max(belief.min_confidence, 
                                      belief.current_confidence - conflict_penalty)
        belief.last_updated = datetime.now()
        
        return conflict_penalty
    
    def resolve_conflicts(self, belief_name: str) -> float:
        """Resolve conflicting evidence and update confidence."""
        if belief_name not in self.beliefs:
            return 0.0
        
        belief = self.beliefs[belief_name]
        
        # Group evidence by type
        positive_evidence = [e for e in belief.evidence_history if e.evidence_type == EvidenceType.POSITIVE]
        negative_evidence = [e for e in belief.evidence_history if e.evidence_type == EvidenceType.NEGATIVE]
        contradictory_evidence = [e for e in belief.evidence_history if e.evidence_type == EvidenceType.CONTRADICTORY]
        
        if not contradictory_evidence:
            return belief.current_confidence
        
        # Calculate net evidence balance
        positive_weight = sum(self._calculate_evidence_weight(e, belief) for e in positive_evidence)
        negative_weight = sum(self._calculate_evidence_weight(e, belief) for e in negative_evidence)
        contradictory_weight = sum(self._calculate_evidence_weight(e, belief) for e in contradictory_evidence)
        
        # Adjust confidence based on evidence balance
        if contradictory_weight > positive_weight + negative_weight:
            # High contradiction - reduce confidence significantly
            belief.current_confidence *= 0.5
        elif contradictory_weight > 0:
            # Some contradiction - reduce confidence moderately
            belief.current_confidence *= 0.8
        
        belief.last_updated = datetime.now()
        return belief.current_confidence


def test_belief_management():
    """Test the belief management system."""
    
    print("=== BELIEF MANAGEMENT SYSTEM TEST ===")
    print()
    
    # Create belief manager
    manager = BeliefManager()
    
    # Test 1: Create beliefs
    print("1. Creating Beliefs:")
    
    temp_belief = manager.create_belief(
        name="temperature_is_high",
        initial_confidence=0.8,
        decay_function=DecayFunction.EXPONENTIAL,
        decay_rate=0.1,
        decay_period=timedelta(hours=1)
    )
    
    server_belief = manager.create_belief(
        name="server_is_healthy",
        initial_confidence=0.9,
        decay_function=DecayFunction.LINEAR,
        decay_rate=0.05,
        decay_period=timedelta(hours=1)
    )
    
    print(f"  Created '{temp_belief.name}' with confidence: {temp_belief.current_confidence}")
    print(f"  Created '{server_belief.name}' with confidence: {server_belief.current_confidence}")
    
    print()
    
    # Test 2: Apply decay
    print("2. Testing Confidence Decay:")
    
    # Simulate time passing by manually updating last_updated
    old_time = datetime.now() - timedelta(hours=2)
    manager.beliefs["temperature_is_high"].last_updated = old_time
    
    decayed_confidence = manager.get_current_confidence("temperature_is_high")
    print(f"  Original confidence: 0.8")
    print(f"  After 2 hours (exponential decay): {decayed_confidence:.3f}")
    
    # Test linear decay
    manager.beliefs["server_is_healthy"].last_updated = old_time
    server_decayed = manager.get_current_confidence("server_is_healthy")
    print(f"  Original confidence: 0.9")
    print(f"  After 2 hours (linear decay): {server_decayed:.3f}")
    
    print()
    
    # Test 3: Update beliefs with evidence
    print("3. Updating Beliefs with Evidence:")
    
    # Add positive evidence
    evidence1 = Evidence(
        content="Temperature sensor reads 30°C",
        confidence=0.9,
        source="sensor_123",
        timestamp=datetime.now(),
        evidence_type=EvidenceType.POSITIVE,
        weight=1.0
    )
    
    manager.update_belief("temperature_is_high", 0.95, evidence1)
    updated_confidence = manager.get_current_confidence("temperature_is_high")
    print(f"  Updated 'temperature_is_high' confidence: {updated_confidence:.3f}")
    
    # Add negative evidence
    evidence2 = Evidence(
        content="Server response time > 5s",
        confidence=0.8,
        source="monitoring_system",
        timestamp=datetime.now(),
        evidence_type=EvidenceType.NEGATIVE,
        weight=1.0
    )
    
    manager.update_belief("server_is_healthy", 0.3, evidence2)
    server_updated = manager.get_current_confidence("server_is_healthy")
    print(f"  Updated 'server_is_healthy' confidence: {server_updated:.3f}")
    
    print()
    
    # Test 4: Contradictory evidence
    print("4. Handling Contradictory Evidence:")
    
    contradictory = Evidence(
        content="Temperature sensor calibrated, shows 22°C",
        confidence=0.85,
        source="calibration_tool",
        timestamp=datetime.now(),
        evidence_type=EvidenceType.CONTRADICTORY,
        weight=1.0
    )
    
    conflict_penalty = manager.add_contradictory_evidence("temperature_is_high", contradictory)
    final_confidence = manager.get_current_confidence("temperature_is_high")
    print(f"  Conflict penalty applied: {conflict_penalty:.3f}")
    print(f"  Final 'temperature_is_high' confidence: {final_confidence:.3f}")
    
    # Resolve conflicts
    resolved_confidence = manager.resolve_conflicts("temperature_is_high")
    print(f"  After conflict resolution: {resolved_confidence:.3f}")
    
    print()
    
    # Test 5: Different decay functions
    print("5. Comparing Decay Functions:")
    
    # Create identical beliefs with different decay functions
    beliefs_info = [
        ("linear_decay", DecayFunction.LINEAR),
        ("exponential_decay", DecayFunction.EXPONENTIAL),
        ("logarithmic_decay", DecayFunction.LOGARITHMIC),
        ("step_decay", DecayFunction.STEP)
    ]
    
    test_beliefs = {}
    for name, decay_func in beliefs_info:
        belief = manager.create_belief(
            name=name,
            initial_confidence=0.9,
            decay_function=decay_func,
            decay_rate=0.1,
            decay_period=timedelta(hours=1)
        )
        test_beliefs[name] = belief
        # Simulate 5 hours passing
        belief.last_updated = datetime.now() - timedelta(hours=5)
    
    print("  Confidence after 5 hours (initial: 0.9):")
    for name, decay_func in beliefs_info:
        current = manager.get_current_confidence(name)
        print(f"    {decay_func.value:12}: {current:.3f}")
    
    return True


if __name__ == '__main__':
    test_belief_management()
    
    print("\n" + "="*60)
    print("Belief management system implemented successfully!")
    print("Features:")
    print("  - Multiple decay functions (linear, exponential, logarithmic, step)")
    print("  - Evidence weighting based on recency and type")
    print("  - Contradictory evidence handling")
    print("  - Conflict resolution mechanisms")
    print("  - Belief state tracking with metadata")
    print("  - Confidence bounds and constraints")
    print()
    print("The BOC language now supports sophisticated belief management")
    print("with dynamic confidence updating and temporal decay for agent collaboration.")