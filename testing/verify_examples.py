"""Summary of all 5 final examples"""
import json
from pathlib import Path

examples = [
    ("Example 1: Detailed E-commerce", "final_examples/example1_detailed_ecommerce/output.json"),
    ("Example 2: Minimal/Vague", "final_examples/example2_minimal_vague/output.json"),
    ("Example 3: Multi-modal Conflict", "final_examples/example3_multimodal_conflict/output.json"),
    ("Example 4: Document PRD", "final_examples/example4_document_prd/output.json"),
    ("Example 5: Contradictory", "final_examples/example5_contradictory/output.json"),
]

print("=" * 80)
print("FINAL EXAMPLES SUMMARY")
print("=" * 80)
print()

for name, path in examples:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    val = data['validation']
    prompt = data['refined_prompt']
    meta = data['processing_metadata']
    
    print(f"{name}")
    print(f"  Completeness: {val['completeness_score']:.2f}")
    print(f"  Valid: {val['is_valid_prompt']}")
    print(f"  Modalities: {', '.join(meta['input_modalities'])}")
    print(f"  Requirements: {len(prompt['requirements'])}")
    print(f"  Constraints: {len(prompt['constraints'])}")
    print(f"  Conflicts: {len(prompt['conflicts_and_ambiguities'])}")
    print(f"  Assumptions: {len(prompt['assumptions'])}")
    print()

print("=" * 80)
print("✓ All 5 diverse examples generated successfully!")
print("✓ See final_examples/README.md for overview")
print("✓ See docs/examples_overview.md for detailed analysis")
