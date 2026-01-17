"""
Main entry point for Prompt Refinement System
"""

import json
from pathlib import Path
from input_processor import InputProcessor
from refiner import PromptRefiner


def refine_prompt(inputs):
    """
    Main function to refine prompts
    
    Args:
        inputs: List of input dicts with type and content/path
    
    Returns:
        Refined prompt structure
    """
    # Step 1: Process inputs
    processor = InputProcessor()
    processed = processor.process_inputs(inputs)
    
    print(f"✓ Processed {len(inputs)} inputs")
    print(f"  Modalities detected: {processed['modalities']}")
    
    # Step 2: Refine with LLM
    refiner = PromptRefiner()
    refined = refiner.refine(processed)
    
    print(f"✓ Refined prompt generated")
    print(f"  Valid: {refined['validation']['is_valid_prompt']}")
    print(f"  Completeness: {refined['validation']['completeness_score']:.2f}")
    
    return refined


def main():
    """Example usage"""
    
    # Example 1: Text only
    print("\n=== Example 1: Text Input ===")
    inputs = [
        {
            'type': 'text',
            'content': 'Build a mobile app like Uber but for electricians.'
        }
    ]
    
    result = refine_prompt(inputs)
    
    # Save output
    output_path = Path('examples/output_example1.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"  Saved to: {output_path}")
    
    # Print key info
    print("\nIntent:")
    print(f"  Purpose: {result['refined_prompt']['intent']['purpose']}")
    print(f"  Confidence: {result['refined_prompt']['intent']['confidence']}")
    
    print("\nRequirements:")
    for req in result['refined_prompt']['requirements'][:3]:
        print(f"  - {req['text']} [{req['status']}]")


if __name__ == '__main__':
    main()
