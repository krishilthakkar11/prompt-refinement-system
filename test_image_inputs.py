"""
Test Suite: Image Input Examples
Tests vision capabilities with product sketches, mockups, and screenshots
"""

import json
from pathlib import Path
from main import refine_prompt


def test_image_input(image_path, test_name, description):
    """Test a single image input"""
    
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Description: {description}")
    print(f"Image: {image_path}")
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        print("Skipping this test.")
        return None
    
    # Prepare input
    inputs = [{'type': 'image', 'path': image_path}]
    
    try:
        # Run refinement
        result = refine_prompt(inputs)
        
        # Print summary
        print(f"\n--- Results ---")
        print(f"Valid: {result['validation']['is_valid_prompt']}")
        print(f"Completeness: {result['validation']['completeness_score']:.2f}")
        
        if not result['validation']['is_valid_prompt']:
            print(f"Rejection Reason: {result['validation']['rejection_reason']}")
        else:
            print(f"Purpose: {result['refined_prompt']['intent']['purpose'][:100]}...")
            print(f"Confidence: {result['refined_prompt']['intent']['confidence']}")
            print(f"Requirements: {len(result['refined_prompt']['requirements'])}")
            print(f"Constraints: {len(result['refined_prompt']['constraints'])}")
        
        # Save result
        output_path = Path(f'examples/test_image_{test_name.replace(" ", "_").lower()}.json')
        output_path.parent.mkdir(exist_ok=True)
        
        test_output = {
            "test_name": test_name,
            "test_description": description,
            "image_path": str(image_path),
            "result": result
        }
        
        with open(output_path, 'w') as f:
            json.dump(test_output, f, indent=2)
        
        print(f"Saved: {output_path}")
        
        return result
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return None


def run_image_tests():
    """Run image input tests"""
    
    print("\n" + "="*80)
    print(" "*20 + "IMAGE INPUT TEST SUITE")
    print("="*80)
    
    # Test cases - update these paths with actual images
    test_cases = [
        {
            "name": "WhatsApp Image Test",
            "description": "User uploaded image for testing",
            "path": "test_images/WhatsApp Image 2026-01-17 at 10.59.27 AM.png"
        }
    ]
    
    results = []
    
    for test in test_cases:
        result = test_image_input(test['path'], test['name'], test['description'])
        if result:
            results.append({
                "test": test['name'],
                "valid": result['validation']['is_valid_prompt'],
                "completeness": result['validation']['completeness_score']
            })
    
    # Summary
    if results:
        print(f"\n\n{'='*80}")
        print("TEST SUITE SUMMARY")
        print(f"{'='*80}")
        print(f"{'Test Name':<40} {'Valid':<10} {'Completeness':<15}")
        print(f"{'-'*80}")
        
        for r in results:
            valid_str = "✓ Yes" if r['valid'] else "✗ No"
            comp_str = f"{r['completeness']:.2f}"
            print(f"{r['test']:<40} {valid_str:<10} {comp_str:<15}")
        
        print(f"\nTotal Tests: {len(results)}")
        print(f"Valid Prompts: {sum(1 for r in results if r['valid'])}")
        print(f"Invalid/Rejected: {sum(1 for r in results if not r['valid'])}")
    else:
        print("\n⚠️  No images found to test.")
        print("\nTo test image inputs:")
        print("1. Create a 'test_images' folder")
        print("2. Add some test images (PNG, JPG)")
        print("3. Update the paths in this script if needed")
        print("4. Run the script again")


if __name__ == '__main__':
    run_image_tests()
