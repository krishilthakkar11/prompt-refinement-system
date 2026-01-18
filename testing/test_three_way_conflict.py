"""Test three-way conflict detection: text vs image vs document"""
from main import refine_prompt
import json

# Simulate the exact scenario the user described
inputs = [
    {
        "type": "text",
        "content": "Build me an app like BookMyShow"
    },
    {
        "type": "image",
        "path": "test_images/WhatsApp Image 2026-01-17 at 10.59.27 AM.png"  # Food delivery app
    },
    {
        "type": "document",
        "path": "test_documents/sample_project_requirements.pdf"  # Smart home automation
    }
]

print("=" * 80)
print("Testing Three-Way Conflict Detection")
print("=" * 80)
print("Text: BookMyShow (movie booking)")
print("Image: Swiggy interface (food delivery)")
print("Document: Smart home automation")
print("=" * 80)
print()

result = refine_prompt(inputs)

print("\n" + "=" * 80)
print("CONFLICTS DETECTED:")
print("=" * 80)

conflicts = result['refined_prompt']['conflicts_and_ambiguities']

if len(conflicts) == 0:
    print("❌ NO CONFLICTS DETECTED - THIS IS WRONG!")
    print("   System should detect 3 different domains")
elif len(conflicts) == 1:
    print(f"⚠️  PARTIAL: Only {len(conflicts)} conflict detected")
    print(f"   Issue: {conflicts[0]['issue']}")
    print(f"   Missing: Conflicts with other modalities")
else:
    print(f"✅ GOOD: {len(conflicts)} conflicts detected")

print()
for i, conflict in enumerate(conflicts, 1):
    print(f"\nConflict {i}:")
    print(f"  Issue: {conflict['issue']}")
    print(f"  Impact: {conflict['impact']}")
    print(f"  Evidence: {json.dumps(conflict['evidence'], indent=4)}")

# Save full output
output_path = 'examples/test_three_way_conflict.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n\nFull output saved to: {output_path}")
