# Example 5: Contradictory Requirements

## Description
Demonstrates detection of logically contradictory and unrealistic requirements.

## Input
Text with multiple logical contradictions:
- "Offline app" + "real-time synchronization" + "cloud backup every 5 minutes"
- "Under 5MB app size" + "HD video calling feature"
- "No internet required" + cloud-dependent features
- "$5,000 budget" + "2 weeks timeline" for complex collaboration app
- "No user registration" + "personalized recommendations"

## Expected Behavior
- Extract all requirements (even contradictory ones)
- Detect logical conflicts
- Flag unrealistic constraints
- High completeness (information is present, just contradictory)

## Actual Results
- **Completeness: 0.87** (High)
- **Requirements: 8** (all contradictory ones captured)
- **Conflicts: 3**
  1. Offline requirement vs real-time sync/cloud backup
  2. 5MB size limit vs HD video calling
  3. Unrealistic $5k budget + 2 week timeline
- **Constraints: 2** (budget, timeline with impact)
- **Valid: Yes**

## What It Shows
- Logic validation and contradiction detection
- Completeness ≠ feasibility (can be high even with conflicts)
- Practical feasibility assessment (budget/timeline validation)
- Detailed conflict descriptions with impact analysis
- System doesn't filter contradictions - documents them
