"""
Interactive PDF/Document Prompt Refinement
Allows user to select a PDF or DOCX file and extract requirements
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
        print(f"📋 REQUIREMENTS ({len(refined['requirements'])} total)")
        print_separator()
        
        # Show first 5, then ask if user wants to see more
        display_count = min(5, len(refined['requirements']))
        for i, req in enumerate(refined['requirements'][:display_count], 1):
            print(f"{i}. {req['text']}")
            print(f"   Status: {req['status']} | Source: {req['source']}")
        
        if len(refined['requirements']) > 5:
            print(f"\n... and {len(refined['requirements']) - 5} more requirements")
    
    # Constraints
    if refined['constraints']:
        print_separator()
        print(f"⚠️  CONSTRAINTS ({len(refined['constraints'])} total)")
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
            print(f"   Impact: {conflict['impact']}")
    
    # Assumptions
    if refined['assumptions']:
        print_separator()
        print(f"💭 ASSUMPTIONS ({len(refined['assumptions'])} total)")
        print_separator()
        display_count = min(3, len(refined['assumptions']))
        for i, assume in enumerate(refined['assumptions'][:display_count], 1):
            print(f"{i}. {assume['assumption']}")
            print(f"   Risk if wrong: {assume['risk_if_wrong']}")
        
        if len(refined['assumptions']) > 3:
            print(f"\n... and {len(refined['assumptions']) - 3} more assumptions")


def save_result(doc_path, result):
    """Save the result to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f'examples/interactive_document_{timestamp}.json')
    output_path.parent.mkdir(exist_ok=True)
    
    output = {
        "timestamp": timestamp,
        "document_path": str(doc_path),
        "result": result
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    return output_path


def main():
    """Interactive document prompt refinement"""
    
    print("\n" + "="*80)
    print(" "*12 + "DOCUMENT PROMPT REFINEMENT SYSTEM")
    print("="*80)
    print("\nThis tool extracts product requirements from PDF and DOCX documents.")
    print("\nBest for:")
    print("  - Product Requirement Documents (PRD)")
    print("  - Technical specifications")
    print("  - Project proposals")
    print("  - Feature documentation")
    print("\nSupported formats: PDF, DOCX")
    print("\nType 'quit' or 'exit' to stop.")
    print("="*80)
    
    while True:
        print("\n" + "-"*80)
        doc_path = input("Enter document file path (or 'quit'): ").strip()
        
        if doc_path.lower() in ['quit', 'exit', '']:
            print("\n👋 Goodbye!")
            break
        
        # Remove quotes if present
        doc_path = doc_path.strip('"').strip("'")
        
        # Check if file exists
        path = Path(doc_path)
        if not path.exists():
            print(f"\n❌ File not found: {doc_path}")
            print("Please check the path and try again.")
            continue
        
        # Check if it's a supported document
        if path.suffix.lower() not in ['.pdf', '.docx']:
            print(f"\n❌ Unsupported file format: {path.suffix}")
            print("Please use PDF or DOCX files.")
            continue
        
        print(f"\n⏳ Extracting text from: {path.name}")
        print("This may take a moment for large documents...")
        
        try:
            # Process document
            inputs = [{'type': 'pdf', 'path': str(path)}]
            result = refine_prompt(inputs)
            
            # Display results
            print_result(result)
            
            # Save option
            print_separator()
            save_choice = input("Save this result? (y/n): ").strip().lower()
            
            if save_choice == 'y':
                output_path = save_result(doc_path, result)
                print(f"✓ Saved to: {output_path}")
            
            # Continue option
            print_separator()
            continue_choice = input("Analyze another document? (y/n): ").strip().lower()
            
            if continue_choice != 'y':
                print("\n👋 Goodbye!")
                break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with a different document.")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()
