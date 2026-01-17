"""
Test Suite: Text Input Examples
Tests the system with 5 diverse text inputs - good, bad, and edge cases
"""

import json
from pathlib import Path
from main import refine_prompt


# Test cases covering different scenarios
TEST_CASES = [
    {
        "name": "Good - Detailed E-commerce Platform",
        "description": "Clear, detailed product request with specific features",
        "input": """
        Build an e-commerce platform for selling handmade crafts. 
        
        Key features needed:
        - User registration and authentication
        - Product catalog with search and filtering
        - Shopping cart and checkout with multiple payment options (credit card, PayPal)
        - Seller dashboard to manage inventory and orders
        - Customer reviews and ratings
        - Mobile-responsive design
        
        Technical requirements:
        - Must handle 10,000 concurrent users
        - Payment processing must be PCI compliant
        - Need admin panel for content moderation
        
        Budget: $50,000
        Timeline: 6 months
        """
    },
    {
        "name": "Bad - Extremely Vague",
        "description": "Minimal information, no clear requirements",
        "input": "I need an app. Something cool for my business."
    },
    {
        "name": "Good - Clear MVP Scope",
        "description": "Well-defined minimal viable product",
        "input": """
        Create a task management web app for small teams (5-10 people).
        
        Core features:
        - Create, assign, and track tasks
        - Set due dates and priorities
        - Simple kanban board view
        - Email notifications for task updates
        
        Out of scope: Time tracking, invoicing, file storage.
        Target launch: Q2 2026
        """
    },
    {
        "name": "Bad - Non-Product Request",
        "description": "Creative writing request, not a product/system",
        "input": "Write me a poem about artificial intelligence and the future of humanity. Make it inspiring and thought-provoking."
    },
    {
        "name": "Edge - Contradictory Requirements",
        "description": "Contains conflicting requirements",
        "input": """
        Build a lightweight mobile app for iOS that doesn't require internet connection.
        
        Features needed:
        - Real-time chat with other users
        - Cloud sync across all devices
        - Live video streaming
        - Works completely offline
        
        Must be under 5MB in size and support all iOS devices from iOS 12 onwards.
        """
    }
]


def run_test_suite():
    """Run all test cases and save results"""
    
    results = []
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"Description: {test['description']}")
        print(f"\nInput Preview: {test['input'][:100]}...")
        
        # Prepare input
        inputs = [{'type': 'text', 'content': test['input']}]
        
        # Run refinement
        try:
            result = refine_prompt(inputs)
            
            # Print summary
            print(f"\n--- Results ---")
            print(f"Valid: {result['validation']['is_valid_prompt']}")
            print(f"Completeness: {result['validation']['completeness_score']:.2f}")
            
            if not result['validation']['is_valid_prompt']:
                print(f"Rejection Reason: {result['validation']['rejection_reason']}")
            else:
                print(f"Purpose: {result['refined_prompt']['intent']['purpose'][:80]}...")
                print(f"Confidence: {result['refined_prompt']['intent']['confidence']}")
                print(f"Requirements: {len(result['refined_prompt']['requirements'])}")
                print(f"Constraints: {len(result['refined_prompt']['constraints'])}")
                print(f"Conflicts: {len(result['refined_prompt']['conflicts_and_ambiguities'])}")
                print(f"Assumptions: {len(result['refined_prompt']['assumptions'])}")
            
            # Save result
            output_path = Path(f'examples/test_text_{i}_{test["name"].split("-")[0].strip().lower()}.json')
            output_path.parent.mkdir(exist_ok=True)
            
            test_output = {
                "test_name": test['name'],
                "test_description": test['description'],
                "input": test['input'],
                "result": result
            }
            
            with open(output_path, 'w') as f:
                json.dump(test_output, f, indent=2)
            
            print(f"Saved: {output_path}")
            
            results.append({
                "test": test['name'],
                "valid": result['validation']['is_valid_prompt'],
                "completeness": result['validation']['completeness_score']
            })
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            results.append({
                "test": test['name'],
                "valid": False,
                "error": str(e)
            })
    
    # Summary
    print(f"\n\n{'='*80}")
    print("TEST SUITE SUMMARY")
    print(f"{'='*80}")
    print(f"{'Test Name':<40} {'Valid':<10} {'Completeness':<15}")
    print(f"{'-'*80}")
    
    for r in results:
        valid_str = "✓ Yes" if r['valid'] else "✗ No"
        comp_str = f"{r.get('completeness', 0):.2f}" if 'completeness' in r else "N/A"
        print(f"{r['test']:<40} {valid_str:<10} {comp_str:<15}")
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Valid Prompts: {sum(1 for r in results if r['valid'])}")
    print(f"Invalid/Rejected: {sum(1 for r in results if not r['valid'])}")


if __name__ == '__main__':
    run_test_suite()
