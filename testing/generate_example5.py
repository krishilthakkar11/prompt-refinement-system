"""Generate refined output for Example 5: Contradictory requirements"""
from main import refine_prompt
import json

with open('final_examples/example5_contradictory/input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

result = refine_prompt([{"type": "text", "content": text}])

with open('final_examples/example5_contradictory/output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✓ Example 5 generated")
print(f"  Completeness: {result['validation']['completeness_score']:.2f}")
print(f"  Valid: {result['validation']['is_valid_prompt']}")
print(f"  Requirements: {len(result['refined_prompt']['requirements'])}")
print(f"  Conflicts: {len(result['refined_prompt']['conflicts_and_ambiguities'])}")
print(f"  Constraints: {len(result['refined_prompt']['constraints'])}")
