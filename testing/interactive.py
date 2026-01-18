"""
Interactive Prompt Refinement Tool
Allows user to enter text inputs and see refined output
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


def save_result(user_input, result):
    """Save the result to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f'examples/interactive_{timestamp}.json')
    output_path.parent.mkdir(exist_ok=True)
    
    output = {
        "timestamp": timestamp,
        "user_input": user_input,
        "result": result
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    return output_path


def main():
    """Interactive prompt refinement"""
    
    print("\n" + "="*80)
    print(" "*20 + "PROMPT REFINEMENT SYSTEM")
    print("="*80)
    print("\nEnter your prompt description below.")
    print("You can describe a product, app, or system you want to build.")
    print("\nTips:")
    print("- Be specific about features and requirements")
    print("- Mention any constraints (budget, timeline, platform)")
    print("- Include technical requirements if known")
    print("\nType 'quit' or 'exit' to stop.")
    print("="*80)
    
    while True:
        print("\n" + "-"*80)
        print("Enter your prompt (press Enter twice when done):")
        print("-"*80)
        
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
        
        user_input = '\n'.join(lines).strip()
        
        if not user_input:
            print("\n⚠️  No input provided. Try again.")
            continue
        
        if user_input.lower() in ['quit', 'exit']:
            print("\n👋 Goodbye!")
            break
        
        print("\n⏳ Processing your input...")
        
        try:
            # Process input
            inputs = [{'type': 'text', 'content': user_input}]
            result = refine_prompt(inputs)
            
            # Display results
            print_result(result)
            
            # Save option
            print_separator()
            save_choice = input("Save this result? (y/n): ").strip().lower()
            
            if save_choice == 'y':
                output_path = save_result(user_input, result)
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
