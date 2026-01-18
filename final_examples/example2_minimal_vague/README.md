# Example 2: Minimal/Vague Input

## Description
Demonstrates handling of extremely minimal input with significant information gaps.

## Input
Single brief sentence: "I need an app for my startup. Something modern and user-friendly. It should help with productivity."

## Expected Behavior
- Lower completeness score
- Inferred requirements
- Explicit assumptions with risk documentation
- Medium confidence

## Actual Results
- **Completeness: 0.65** (Moderate)
- **Requirements: 2** (both inferred)
- **Assumptions: 1** (with risk assessment)
- **Valid: Yes**
- **Confidence: Medium**

## What It Shows
- System doesn't hallucinate details when information is missing
- Completeness score correctly reflects gaps
- Assumptions are made explicit with documented risks
- Transparency principle in action
