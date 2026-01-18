"""Generate refined output for Example 4: Document-heavy"""
from main import refine_prompt
import json

result = refine_prompt([
    {"type": "document", "path": "final_examples/example4_document_prd/input.pdf"}
])

with open('final_examples/example4_document_prd/output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✓ Example 4 generated")
print(f"  Completeness: {result['validation']['completeness_score']:.2f}")
print(f"  Valid: {result['validation']['is_valid_prompt']}")
print(f"  Requirements: {len(result['refined_prompt']['requirements'])}")
print(f"  Deliverables: {len(result['refined_prompt']['deliverables'])}")
