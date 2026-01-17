# Design Decision: Essential vs Optional Information

## Problem Statement

The core challenge in prompt refinement is determining **what information is required** to create a useful, actionable prompt versus **what information adds value but isn't blocking**.

## Design Philosophy

I organized information by **semantic certainty** rather than priority or actors:

**Essential Information** = What you need to know to start building
**Optional Information** = What helps you build it better

This mirrors how real product development works: you can start with a vision and core features, but constraints like budget and timeline can be discovered or negotiated.

---

## Essential Information (Must Have)

### 1. Intent Purpose
**Why it's essential:** Without knowing WHAT needs to be built, nothing else matters.

**Validation Rule:**
```python
'intent.purpose': {
    'min_length': 10,
    'rejection_reason': 'No clear product/system intent'
}
```

**Examples:**
- ✅ "Build a food delivery mobile app"
- ❌ "Make something cool"

### 2. Problem Being Solved
**Why it's essential:** Defines the WHY behind the request. Without it, you can't validate if features make sense.

**Validation Rule:**
```python
'intent.problem_being_solved': {
    'min_length': 10,
    'rejection_reason': 'Problem statement missing or unclear'
}
```

**Examples:**
- ✅ "Users struggle to find nearby restaurants quickly"
- ❌ "" (empty)

### 3. At Least One Requirement
**Why it's essential:** A prompt with zero requirements is not actionable.

**Validation Rule:**
```python
'requirements': {
    'min_count': 1,
    'rejection_reason': 'No actionable requirements identified'
}
```

**Examples:**
- ✅ ["User can search restaurants", "User can place orders"]
- ❌ [] (empty list)

---

## Optional Information (Nice to Have)

### 1. Constraints
**Why it's optional:** Many real projects start without knowing budget or timeline upfront.

**Value when present:**
- Helps scope the solution
- Prevents over-engineering
- Sets realistic expectations

**Examples:**
- Budget: $50,000
- Timeline: 6 months
- Platform: Must support iOS 14+

### 2. Deliverables
**Why it's optional:** These can often be inferred from requirements.

**Value when present:**
- Makes expectations explicit
- Helps with project planning
- Useful for proposals/contracts

**Examples:**
- iOS mobile app
- API documentation
- Admin dashboard

### 3. Assumptions
**Why it's optional:** These emerge during analysis, not from the input.

**Value when present:**
- Documents what was inferred
- Highlights risks
- Makes reasoning transparent

**Examples:**
- "Assuming single-city launch initially"
- "Assuming English-only for MVP"

---

## Completeness Scoring

I weighted information by **impact on actionability**:

```python
COMPLETENESS_WEIGHTS = {
    'intent': 0.30,           # 30% - Knowing what to build
    'requirements': 0.40,      # 40% - Knowing how it should work
    'constraints': 0.15,       # 15% - Knowing limitations
    'deliverables': 0.10,      # 10% - Knowing what to ship
    'no_conflicts': 0.05       # 5% - Having clarity
}
```

### Rationale:

**Requirements = 40%** (highest)
Because without specific functionality, you can't build anything. This is the core value of refinement.

**Intent = 30%** (second)
Because clear purpose and problem drive all decisions.

**Constraints = 15%**
Important for scoping but can be discovered later.

**Deliverables = 10%**
Often derivable from requirements.

**No Conflicts = 5%**
Bonus for clarity.

---

## Why This Design Beats Alternatives

### ❌ Alternative 1: Reject if ANY field is missing
**Problem:** Too strict. Real-world prompts are often incomplete.

**Example:** "Build Uber for plumbers" has no budget/timeline but is valid.

### ❌ Alternative 2: Accept everything, no validation
**Problem:** Garbage in, garbage out. Produces useless outputs.

**Example:** "Make an app" would pass validation.

### ✅ My Approach: Essential + Scoring
**Advantage:** 
- Rejects truly unusable inputs
- Accepts imperfect but actionable inputs
- Scores completeness to show quality

**Example:** 
- "Build Uber for plumbers" → Valid, 0.60 score (missing details)
- "Build e-commerce with [10 features]" → Valid, 0.95 score (comprehensive)
- "Write a poem" → Invalid (no product intent)

---

## Edge Cases Handled

### Case 1: Vague but Valid
**Input:** "I need a food delivery app"

**Decision:** ACCEPT with low completeness (0.50-0.60)
- Has intent ✓
- Has problem (implicit) ✓
- Has 1+ requirement (delivery functionality) ✓

### Case 2: Detailed but Non-Product
**Input:** Long essay about AI ethics

**Decision:** REJECT
- No product/system intent ✗

### Case 3: Requirements without Context
**Input:** List of 20 features with no explanation

**Decision:** ACCEPT with medium completeness (0.70-0.80)
- Intent might be inferred ✓
- Has requirements ✓
- But lacks problem statement (lower score)

### Case 4: Conflicting Information
**Input:** "Build offline app that syncs to cloud"

**Decision:** ACCEPT but flag conflict
- Intent clear ✓
- Requirements clear ✓
- Conflict documented → Lower completeness

---

## Implementation Details

### Validation Happens in Two Stages:

1. **LLM Extraction** (refiner.py)
   - GPT-4 extracts information
   - Makes best effort to populate template

2. **Explicit Validation** (validation.py)
   - Checks essential fields programmatically
   - Calculates completeness score
   - Returns pass/fail + detailed reasoning

### Why This Separation?

**LLM handles:** Ambiguity, inference, interpretation
**Code handles:** Rules, consistency, explainability

This makes the system **auditable** - you can trace exactly why a prompt was rejected.

---

## Self-Critique

### Strengths:
- ✅ Clear distinction between must-have and nice-to-have
- ✅ Flexible enough for real-world use
- ✅ Strict enough to reject garbage
- ✅ Explainable scoring

### Weaknesses:
- ⚠️ Magic numbers in weights (why 40% not 35%?)
- ⚠️ Min length of 10 chars is arbitrary
- ⚠️ Doesn't account for domain-specific needs

### Future Improvements:
- Make weights configurable per domain
- Add user feedback loop to tune thresholds
- Support custom validation rules per industry

---

## Conclusion

**Essential vs Optional is not about perfectionism - it's about actionability.**

My design ensures that every accepted prompt contains enough information to start a meaningful conversation with a development team, while being forgiving enough to work with real-world, imperfect inputs.

The completeness score then provides a quality signal without being binary pass/fail.
