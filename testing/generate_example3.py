"""Generate refined output for Example 3: Multi-modal with conflicts"""
from main import refine_prompt
import json

# Read text
with open('final_examples/example3_multimodal_conflict/input_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Process all three inputs
result = refine_prompt([
    {"type": "text", "content": text},
    {"type": "image", "path": "final_examples/example3_multimodal_conflict/input_image.png"},
    {"type": "document", "path": "final_examples/example3_multimodal_conflict/input_document.pdf"}
])

with open('final_examples/example3_multimodal_conflict/output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✓ Example 3 generated")
print(f"  Completeness: {result['validation']['completeness_score']:.2f}")
print(f"  Valid: {result['validation']['is_valid_prompt']}")
print(f"  Modalities: {result['processing_metadata']['input_modalities']}")
print(f"  Requirements: {len(result['refined_prompt']['requirements'])}")
print(f"  Conflicts: {len(result['refined_prompt']['conflicts_and_ambiguities'])}")
