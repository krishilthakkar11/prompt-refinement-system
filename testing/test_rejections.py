"""
Test Suite: Rejection Examples
5 text inputs that should be REJECTED by the validation system
"""

import json
from pathlib import Path
from main import refine_prompt


REJECTION_TEST_CASES = [
    {
        "name": "Empty/Nonsense Input",
        "description": "No meaningful content",
        "input": "hmm... yeah... uh... ok",
        "expected_reason": "No clear product/system intent"
    },
    {
        "name": "Pure Question",
        "description": "Just asking a question, no product intent",
        "input": "What is the best way to learn Python? Can you recommend some resources?",
        "expected_reason": "No clear product/system intent"
    },
    {
        "name": "Creative Writing Request",
        "description": "Asking for creative content, not a product",
        "input": "Write me a short story about a robot who falls in love with a toaster. Make it emotional and touching.",
        "expected_reason": "No clear product/system intent"
    },
    {
        "name": "Abstract Philosophy",
        "description": "Philosophical discussion with no actionable intent",
        "input": "The nature of consciousness is fascinating. What does it mean to be truly aware? Can machines ever achieve sentience?",
        "expected_reason": "No clear product/system intent"
    },
    {
        "name": "Pure Greeting",
        "description": "Just a greeting, no request",
        "input": "Hello! How are you doing today?",
        "expected_reason": "No clear product/system intent"
    }
]


def test_rejections():
    """Test that the system correctly rejects invalid inputs"""
    
    print("\n" + "="*80)
    print(" "*20 + "REJECTION TEST SUITE")
    print("="*80)
    print("\nTesting inputs that SHOULD BE REJECTED\n")
    
    results = []
    
    for i, test in enumerate(REJECTION_TEST_CASES, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"Description: {test['description']}")
        print(f"Input: \"{test['input']}\"")
        print(f"Expected rejection reason: {test['expected_reason']}")
        
        # Prepare input
        inputs = [{'type': 'text', 'content': test['input']}]
        
        try:
            # Run refinement
            result = refine_prompt(inputs)
            
            validation = result['validation']
            
            print(f"\n--- Results ---")
            print(f"Valid: {validation['is_valid_prompt']}")
            print(f"Completeness: {validation['completeness_score']:.2f}")
            
            if not validation['is_valid_prompt']:
                print(f"✓ CORRECTLY REJECTED")
                print(f"Rejection Reason: {validation['rejection_reason']}")
                status = "✓ Correct"
            else:
                print(f"✗ INCORRECTLY ACCEPTED")
                print(f"Purpose extracted: {result['refined_prompt']['intent']['purpose']}")
                status = "✗ Should reject"
            
            # Save result
            output_path = Path(f'examples/rejection_test_{i}.json')
            output_path.parent.mkdir(exist_ok=True)
            
            test_output = {
                "test_name": test['name'],
                "test_description": test['description'],
                "input": test['input'],
                "expected_rejection": test['expected_reason'],
                "result": result
            }
            
            with open(output_path, 'w') as f:
                json.dump(test_output, f, indent=2)
            
            results.append({
                "test": test['name'],
                "should_reject": True,
                "was_rejected": not validation['is_valid_prompt'],
                "status": status,
                "completeness": validation['completeness_score']
            })
        
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            results.append({
                "test": test['name'],
                "should_reject": True,
                "was_rejected": False,
                "status": "✗ Error",
                "error": str(e)
            })
    
    # Summary
    print(f"\n\n{'='*80}")
    print("REJECTION TEST SUMMARY")
    print(f"{'='*80}")
    print(f"{'Test Name':<35} {'Should Reject':<15} {'Was Rejected':<15} {'Status'}")
    print(f"{'-'*80}")
    
    for r in results:
        should = "Yes" if r['should_reject'] else "No"
        was = "Yes" if r['was_rejected'] else "No"
        print(f"{r['test']:<35} {should:<15} {was:<15} {r['status']}")
    
    correct_rejections = sum(1 for r in results if r.get('was_rejected') == True)
    incorrect_accepts = sum(1 for r in results if r.get('was_rejected') == False and 'error' not in r)
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Correctly Rejected: {correct_rejections}")
    print(f"Incorrectly Accepted: {incorrect_accepts}")
    
    if correct_rejections == len(results):
        print(f"\n🎉 ALL TESTS PASSED - System correctly rejects invalid inputs!")
    else:
        print(f"\n⚠️  Some inputs were not rejected correctly. Review validation logic.")


if __name__ == '__main__':
    test_rejections()
