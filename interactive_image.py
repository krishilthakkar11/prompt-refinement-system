"""
Interactive Image Prompt Refinement
Allows user to select an image file and see the refined output
"""

import json
from pathlib import Path
from datetime import datetime
from main import refine_prompt


def print_separator():
    print("\n" + "="*80 + "\n")


def print_result(result):
    """Pretty print the refined prompt result"""
    
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
    
    # Requirements
    if refined['requirements']:
        print_separator()
        print("📋 REQUIREMENTS")
        print_separator()
        for i, req in enumerate(refined['requirements'], 1):
            print(f"{i}. {req['text']}")
            print(f"   Status: {req['status']} | Source: {req['source']}")
    
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
    
    # Conflicts
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


def save_result(image_path, result):
    """Save the result to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f'examples/interactive_image_{timestamp}.json')
    output_path.parent.mkdir(exist_ok=True)
    
    output = {
        "timestamp": timestamp,
        "image_path": str(image_path),
        "result": result
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    return output_path


def main():
    """Interactive image prompt refinement"""
    
    print("\n" + "="*80)
    print(" "*15 + "IMAGE PROMPT REFINEMENT SYSTEM")
    print("="*80)
    print("\nThis tool analyzes images (sketches, wireframes, mockups, screenshots)")
    print("and extracts product requirements from them.")
    print("\nSupported formats: PNG, JPG, JPEG, GIF, BMP")
    print("\nType 'quit' or 'exit' to stop.")
    print("="*80)
    
    while True:
        print("\n" + "-"*80)
        image_path = input("Enter image file path (or 'quit'): ").strip()
        
        if image_path.lower() in ['quit', 'exit', '']:
            print("\n👋 Goodbye!")
            break
        
        # Remove quotes if present
        image_path = image_path.strip('"').strip("'")
        
        # Check if file exists
        path = Path(image_path)
        if not path.exists():
            print(f"\n❌ File not found: {image_path}")
            print("Please check the path and try again.")
            continue
        
        # Check if it's an image
        if path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            print(f"\n❌ Unsupported file format: {path.suffix}")
            print("Please use PNG, JPG, JPEG, GIF, or BMP.")
            continue
        
        print(f"\n⏳ Analyzing image: {path.name}")
        
        try:
            # Process image
            inputs = [{'type': 'image', 'path': str(path)}]
            result = refine_prompt(inputs)
            
            # Display results
            print_result(result)
            
            # Save option
            print_separator()
            save_choice = input("Save this result? (y/n): ").strip().lower()
            
            if save_choice == 'y':
                output_path = save_result(image_path, result)
                print(f"✓ Saved to: {output_path}")
            
            # Continue option
            print_separator()
            continue_choice = input("Analyze another image? (y/n): ").strip().lower()
            
            if continue_choice != 'y':
                print("\n👋 Goodbye!")
                break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with a different image.")


if __name__ == '__main__':
    main()
