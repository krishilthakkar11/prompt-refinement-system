"""Generate refined output for Example 1: Detailed E-commerce"""
from main import refine_prompt
import json

# Read input
with open('final_examples/example1_detailed_ecommerce/input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Process
result = refine_prompt([{"type": "text", "content": text}])

# Save output
with open('final_examples/example1_detailed_ecommerce/output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✓ Example 1 generated")
print(f"  Completeness: {result['validation']['completeness_score']:.2f}")
print(f"  Valid: {result['validation']['is_valid_prompt']}")
print(f"  Requirements: {len(result['refined_prompt']['requirements'])}")
print(f"  Constraints: {len(result['refined_prompt']['constraints'])}")
print(f"  Conflicts: {len(result['refined_prompt']['conflicts_and_ambiguities'])}")
