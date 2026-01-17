"""Quick test of generated text prompt feature"""
from main import refine_prompt
import json

# Test with a detailed example
text = """
Build an e-commerce platform for selling handmade crafts.

Key features needed:
- Product catalog with search and filters
- Shopping cart and checkout with payment integration
- Seller dashboard for managing inventory
- Customer reviews and ratings
- Mobile responsive design

Budget: $50,000
Timeline: 6 months
Target audience: Craft enthusiasts in US and Canada
"""

result = refine_prompt([{"type": "text", "content": text}])

print("=" * 80)
print("STRUCTURED OUTPUT:")
print("=" * 80)
print(f"Valid: {result['validation']['is_valid_prompt']}")
print(f"Completeness: {result['validation']['completeness_score']}")
print(f"Requirements: {len(result['refined_prompt']['requirements'])}")
print()

print("=" * 80)
print("GENERATED TEXT PROMPT:")
print("=" * 80)
print(result['generated_text_prompt'])
print()

# Save full output
with open('examples/bonus_example.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\nFull output saved to: examples/bonus_example.json")
