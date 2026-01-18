"""
Interactive Multi-Modal Prompt Refinement
Allows user to enter text AND image together
"""

import json
from pathlib import Path
from datetime import datetime
from main import refine_prompt


def print_separator():
    print("\n" + "="*80 + "\n")


def print_result(result):
    """Pretty print the refined prompt result with source tracking"""
    
    validation = result['validation']
    
    print_separator()
    print("📊 VALIDATION RESULTS")
    print_separator()
    print(f"Valid Prompt: {'✓ YES' if validation['is_valid_prompt'] else '✗ NO'}")
    print(f"Completeness Score: {validation['completeness_score']:.2f}")
    
    if not validation['is_valid_prompt']:
        print(f"Rejection Reason: {validation['rejection_reason']}")
        return
    
    refined = result['refined_prompt']
    
    # Intent
    print_separator()
    print("🎯 INTENT")
    print_separator()
    print(f"Purpose: {refined['intent']['purpose']}")
    print(f"Problem: {refined['intent']['problem_being_solved']}")
    print(f"Domain: {refined['intent']['domain']}")
    print(f"Confidence: {refined['intent']['confidence'].upper()}")
    
    # Requirements - grouped by source
    if refined['requirements']:
        print_separator()
        print("📋 REQUIREMENTS")
        print_separator()
        
        text_reqs = [r for r in refined['requirements'] if r['source'] == 'text']
        image_reqs = [r for r in refined['requirements'] if r['source'] == 'image']
        
        if text_reqs:
            print("From TEXT:")
            for i, req in enumerate(text_reqs, 1):
                print(f"  {i}. {req['text']}")
                print(f"     Status: {req['status']}")
        
        if image_reqs:
            print("\nFrom IMAGE:")
            for i, req in enumerate(image_reqs, 1):
                print(f"  {i}. {req['text']}")
                print(f"     Status: {req['status']}")
    
    # Constraints
    if refined['constraints']:
        print_separator()
        print("⚠️  CONSTRAINTS")
        print_separator()
        for i, const in enumerate(refined['constraints'], 1):
            print(f"{i}. {const['text']}")
            print(f"   Status: {const['status']}")
            print(f"   Impact: {const['impact']}")
    
    # Deliverables
    if refined['deliverables']:
        print_separator()
        print("📦 DELIVERABLES")
        print_separator()
        for i, deliv in enumerate(refined['deliverables'], 1):
            print(f"{i}. {deliv['item']} (Confidence: {deliv['confidence']})")
    
    # Conflicts - IMPORTANT for multi-modal
    if refined['conflicts_and_ambiguities']:
        print_separator()
        print("⚡ CONFLICTS & AMBIGUITIES")
        print_separator()
        for i, conflict in enumerate(refined['conflicts_and_ambiguities'], 1):
            print(f"{i}. {conflict['issue']}")
            print(f"   Evidence: {json.dumps(conflict['evidence'], indent=6)}")
            print(f"   Impact: {conflict['impact']}")
    
    # Assumptions
    if refined['assumptions']:
        print_separator()
        print("💭 ASSUMPTIONS")
        print_separator()
        for i, assume in enumerate(refined['assumptions'], 1):
            print(f"{i}. {assume['assumption']}")
            print(f"   Risk if wrong: {assume['risk_if_wrong']}")


def save_result(text_input, image_path, result):
    """Save the result to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f'examples/interactive_multimodal_{timestamp}.json')
    output_path.parent.mkdir(exist_ok=True)
    
    output = {
        "timestamp": timestamp,
        "text_input": text_input,
        "image_path": str(image_path),
        "result": result
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    return output_path


def main():
    """Interactive multi-modal prompt refinement"""
    
    print("\n" + "="*80)
    print(" "*12 + "MULTI-MODAL PROMPT REFINEMENT SYSTEM")
    print("="*80)
    print("\nThis tool analyzes BOTH text and image inputs together.")
    print("Perfect for testing:")
    print("  - Complementary information (text + UI mockup)")
    print("  - Conflicting requirements (text says mobile, image shows desktop)")
    print("  - Vague text with detailed image reference")
    print("\nType 'quit' or 'exit' to stop.")
    print("="*80)
    
    while True:
        print("\n" + "-"*80)
        print("STEP 1: Enter your text description")
        print("-"*80)
        print("(Press Enter twice when done)")
        
        lines = []
        empty_count = 0
        
        while True:
            line = input()
            if line.strip() == '':
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        
        text_input = '\n'.join(lines).strip()
        
        if not text_input:
            print("\n⚠️  No text provided.")
            continue
        
        if text_input.lower() in ['quit', 'exit']:
            print("\n👋 Goodbye!")
            break
        
        print("\n" + "-"*80)
        print("STEP 2: Enter image file path")
        print("-"*80)
        image_path = input("Image path (or 'skip' for text only): ").strip()
        
        if image_path.lower() in ['quit', 'exit']:
            print("\n👋 Goodbye!")
            break
        
        # Build inputs
        inputs = [{'type': 'text', 'content': text_input}]
        
        if image_path.lower() != 'skip':
            # Remove quotes if present
            image_path = image_path.strip('"').strip("'")
            
            # Check if file exists
            path = Path(image_path)
            if not path.exists():
                print(f"\n⚠️  Image not found: {image_path}")
                print("Continuing with text only...")
            elif path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                print(f"\n⚠️  Unsupported file format: {path.suffix}")
                print("Continuing with text only...")
            else:
                inputs.append({'type': 'image', 'path': str(path)})
                print(f"✓ Image added: {path.name}")
        
        print(f"\n⏳ Processing {len(inputs)} input(s)...")
        
        try:
            # Process inputs
            result = refine_prompt(inputs)
            
            # Display results
            print_result(result)
            
            # Save option
            print_separator()
            save_choice = input("Save this result? (y/n): ").strip().lower()
            
            if save_choice == 'y':
                img_path = inputs[1]['path'] if len(inputs) > 1 else 'none'
                output_path = save_result(text_input, img_path, result)
                print(f"✓ Saved to: {output_path}")
            
            # Continue option
            print_separator()
            continue_choice = input("Process another prompt? (y/n): ").strip().lower()
            
            if continue_choice != 'y':
                print("\n👋 Goodbye!")
                break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again.")


if __name__ == '__main__':
    main()
