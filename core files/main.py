"""
Main Entry Point for Multi-Modal Prompt Refinement System

This module provides the primary interface for refining diverse inputs
(text, images, documents) into a structured, standardized prompt template.

Example:
    >>> from main import refine_prompt
    >>> result = refine_prompt([
    ...     {"type": "text", "content": "Build an e-commerce app"},
    ...     {"type": "image", "path": "mockup.png"}
    ... ])
    >>> print(result['validation']['completeness_score'])
    0.85
"""

import json
from pathlib import Path
from input_processor import InputProcessor
from refiner import PromptRefiner


def refine_prompt(inputs):
    """
    Refine multi-modal inputs into structured prompt template.
    
    This is the main entry point for the system. It processes inputs,
    extracts information, validates completeness, and returns a structured
    prompt with source attribution and conflict detection.
    
    Args:
        inputs (List[Dict]): List of input dictionaries. Each dict must have:
            - type (str): One of 'text', 'image', 'document'
            - For text: 'content' (str) - the actual text
            - For image/document: 'path' (str) - file path
            
            Examples:
                [{"type": "text", "content": "Build a food delivery app"}]
                [{"type": "image", "path": "ui_design.png"}]
                [{"type": "document", "path": "requirements.pdf"}]
                [
                    {"type": "text", "content": "Build BookMyShow"},
                    {"type": "image", "path": "swiggy.png"}
                ]
    
    Returns:
        Dict: Refined prompt structure containing:
            - refined_prompt (dict): Structured template with:
                - intent: Purpose, problem, domain, confidence
                - requirements: Array with text, status, source
                - constraints: Limitations with impact
                - deliverables: Expected outputs
                - conflicts_and_ambiguities: Multi-modal conflicts
                - assumptions: Explicit assumptions with risk
            - validation (dict): 
                - is_valid_prompt (bool)
                - completeness_score (float): 0.0 to 1.0
                - rejection_reason (str or None)
            - processing_metadata (dict):
                - input_modalities (list)
                - timestamp (str)
            - generated_text_prompt (str): Human-readable version
    
    Example:
        >>> result = refine_prompt([{
        ...     "type": "text",
        ...     "content": "Create a task management app for small teams"
        ... }])
        >>> result['validation']['completeness_score']
        0.84
        >>> result['refined_prompt']['intent']['purpose']
        'Create a task management web application'
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
    """
    Demonstrate example usage of the prompt refinement system.
    
    This function shows how to:
    - Process a simple text input
    - Save the output to a file
    - Access key fields from the result
    
    Run with: python main.py
    """
    
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
