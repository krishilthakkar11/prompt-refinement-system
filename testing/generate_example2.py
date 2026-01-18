"""Generate refined output for Example 2: Minimal/Vague"""
from main import refine_prompt
import json

with open('final_examples/example2_minimal_vague/input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

result = refine_prompt([{"type": "text", "content": text}])

with open('final_examples/example2_minimal_vague/output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✓ Example 2 generated")
print(f"  Completeness: {result['validation']['completeness_score']:.2f}")
print(f"  Valid: {result['validation']['is_valid_prompt']}")
print(f"  Requirements: {len(result['refined_prompt']['requirements'])}")
print(f"  Assumptions: {len(result['refined_prompt']['assumptions'])}")
