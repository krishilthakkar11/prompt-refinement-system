"""
Test Suite: Multi-Modal Input (Text + Image)
Tests the system with combined text and image inputs
"""

import json
from pathlib import Path
from main import refine_prompt


def test_multimodal(text, image_path, test_name, description):
    """Test text + image input together"""
    
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Description: {description}")
    print(f"\nText Input: {text[:100]}...")
    print(f"Image: {image_path}")
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        print("Skipping this test.")
        return None
    
    # Prepare inputs - both text and image
    inputs = [
        {'type': 'text', 'content': text},
        {'type': 'image', 'path': image_path}
    ]
    
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
            print(f"\nPurpose: {result['refined_prompt']['intent']['purpose']}")
            print(f"Confidence: {result['refined_prompt']['intent']['confidence']}")
            print(f"\nRequirements: {len(result['refined_prompt']['requirements'])}")
            
            # Show requirements by source
            text_reqs = [r for r in result['refined_prompt']['requirements'] if r['source'] == 'text']
            image_reqs = [r for r in result['refined_prompt']['requirements'] if r['source'] == 'image']
            
            print(f"  - From text: {len(text_reqs)}")
            print(f"  - From image: {len(image_reqs)}")
            
            print(f"\nConstraints: {len(result['refined_prompt']['constraints'])}")
            print(f"Conflicts: {len(result['refined_prompt']['conflicts_and_ambiguities'])}")
            
            if result['refined_prompt']['conflicts_and_ambiguities']:
                print("\n⚡ CONFLICTS DETECTED:")
                for conflict in result['refined_prompt']['conflicts_and_ambiguities']:
                    print(f"  - {conflict['issue']}")
        
        # Save result
        output_path = Path(f'examples/test_multimodal_{test_name.replace(" ", "_").lower()}.json')
        output_path.parent.mkdir(exist_ok=True)
        
        test_output = {
            "test_name": test_name,
            "test_description": description,
            "text_input": text,
            "image_path": str(image_path),
            "result": result
        }
        
        with open(output_path, 'w') as f:
            json.dump(test_output, f, indent=2)
        
        print(f"\nSaved: {output_path}")
        
        return result
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return None


def run_multimodal_tests():
    """Run multi-modal test cases"""
    
    print("\n" + "="*80)
    print(" "*15 + "MULTI-MODAL INPUT TEST SUITE")
    print("="*80)
    
    # First, check what images are available
    test_images_dir = Path("test_images")
    if not test_images_dir.exists():
        print("\n❌ test_images directory not found!")
        return
    
    available_images = list(test_images_dir.glob("*.png")) + list(test_images_dir.glob("*.jpg"))
    
    if not available_images:
        print("\n❌ No images found in test_images directory!")
        return
    
    # Use the first available image
    test_image = str(available_images[0])
    print(f"\nUsing image: {test_image}")
    
    # Test cases
    test_cases = [
        {
            "name": "Complementary Inputs",
            "description": "Text and image provide complementary information",
            "text": """
            Build a food delivery app similar to Swiggy or Zomato.
            
            Key requirements:
            - User authentication and profiles
            - Real-time order tracking with GPS
            - Multiple payment options (card, wallet, cash)
            - Restaurant ratings and reviews
            - Push notifications for order updates
            
            Budget: $30,000
            Timeline: 4 months
            Platform: iOS and Android
            """,
            "image": test_image
        },
        {
            "name": "Conflicting Platform",
            "description": "Text says mobile, image might show desktop",
            "text": """
            Build a desktop application for restaurant management.
            Must run on Windows 10 and above.
            Should include inventory management and billing features.
            """,
            "image": test_image
        },
        {
            "name": "Minimal Text + Image",
            "description": "Vague text, detailed image",
            "text": "I want to build a food app. See the image for design reference.",
            "image": test_image
        },
        {
            "name": "Detailed Text + Reference Image",
            "description": "Complete text specification with image as UI reference",
            "text": """
            Create a food ordering platform with the following features:
            
            Core Features:
            - Browse restaurants by cuisine, rating, delivery time
            - Advanced search and filters
            - Shopping cart with multiple items from same restaurant
            - Scheduled ordering (order for later)
            - Re-order from history
            - Live order tracking
            - In-app chat with delivery person
            
            Technical Requirements:
            - Support 50,000 concurrent users
            - Sub-3-second page load time
            - 99.9% uptime SLA
            - GDPR compliant
            
            The attached image shows the desired UI style and layout.
            """,
            "image": test_image
        }
    ]
    
    results = []
    
    for test in test_cases:
        result = test_multimodal(test['text'], test['image'], test['name'], test['description'])
        if result:
            results.append({
                "test": test['name'],
                "valid": result['validation']['is_valid_prompt'],
                "completeness": result['validation']['completeness_score'],
                "conflicts": len(result['refined_prompt']['conflicts_and_ambiguities'])
            })
    
    # Summary
    if results:
        print(f"\n\n{'='*80}")
        print("TEST SUITE SUMMARY")
        print(f"{'='*80}")
        print(f"{'Test Name':<40} {'Valid':<8} {'Complete':<10} {'Conflicts'}")
        print(f"{'-'*80}")
        
        for r in results:
            valid_str = "✓" if r['valid'] else "✗"
            comp_str = f"{r['completeness']:.2f}"
            conf_str = f"{r['conflicts']}"
            print(f"{r['test']:<40} {valid_str:<8} {comp_str:<10} {conf_str}")
        
        print(f"\nTotal Tests: {len(results)}")
        print(f"Valid Prompts: {sum(1 for r in results if r['valid'])}")
        print(f"With Conflicts: {sum(1 for r in results if r['conflicts'] > 0)}")


if __name__ == '__main__':
    run_multimodal_tests()
