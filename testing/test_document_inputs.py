"""
Test Suite: PDF/Document Input Examples
Tests document parsing and requirement extraction from PDFs
"""

import json
from pathlib import Path
from main import refine_prompt


def test_document_input(doc_path, test_name, description):
    """Test a single document input"""
    
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Description: {description}")
    print(f"Document: {doc_path}")
    
    # Check if document exists
    if not Path(doc_path).exists():
        print(f"❌ Document not found: {doc_path}")
        print("Skipping this test.")
        return None
    
    # Prepare input
    inputs = [{'type': 'pdf', 'path': doc_path}]
    
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
            print(f"\nPurpose: {result['refined_prompt']['intent']['purpose'][:100]}...")
            print(f"Confidence: {result['refined_prompt']['intent']['confidence']}")
            print(f"Requirements: {len(result['refined_prompt']['requirements'])}")
            print(f"Constraints: {len(result['refined_prompt']['constraints'])}")
            print(f"Deliverables: {len(result['refined_prompt']['deliverables'])}")
            
            # Show first few requirements
            if result['refined_prompt']['requirements']:
                print("\nFirst 3 Requirements:")
                for i, req in enumerate(result['refined_prompt']['requirements'][:3], 1):
                    print(f"  {i}. {req['text'][:80]}...")
        
        # Save result
        output_path = Path(f'examples/test_document_{test_name.replace(" ", "_").lower()}.json')
        output_path.parent.mkdir(exist_ok=True)
        
        test_output = {
            "test_name": test_name,
            "test_description": description,
            "document_path": str(doc_path),
            "result": result
        }
        
        with open(output_path, 'w') as f:
            json.dump(test_output, f, indent=2)
        
        print(f"\nSaved: {output_path}")
        
        return result
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def run_document_tests():
    """Run document input tests"""
    
    print("\n" + "="*80)
    print(" "*18 + "DOCUMENT INPUT TEST SUITE")
    print("="*80)
    
    # Check for documents
    test_docs_dir = Path("test_documents")
    if not test_docs_dir.exists():
        test_docs_dir.mkdir(exist_ok=True)
    
    # Find available PDFs
    available_pdfs = list(test_docs_dir.glob("*.pdf")) + list(test_docs_dir.glob("*.docx"))
    
    if not available_pdfs:
        print("\n⚠️  No documents found in test_documents directory!")
        print("\nTo test document inputs:")
        print("1. Add PDF or DOCX files to the 'test_documents' folder")
        print("2. Files can contain:")
        print("   - Product requirement documents (PRD)")
        print("   - Project specifications")
        print("   - Technical documentation")
        print("   - Feature descriptions")
        print("3. Run this script again")
        return
    
    print(f"\nFound {len(available_pdfs)} document(s) to test:")
    for doc in available_pdfs:
        print(f"  - {doc.name}")
    
    results = []
    
    for doc_path in available_pdfs:
        # Generate test name from filename
        test_name = doc_path.stem.replace("_", " ").title()
        description = f"Testing document extraction from {doc_path.suffix.upper()} file"
        
        result = test_document_input(str(doc_path), test_name, description)
        
        if result:
            results.append({
                "test": test_name,
                "document": doc_path.name,
                "valid": result['validation']['is_valid_prompt'],
                "completeness": result['validation']['completeness_score'],
                "requirements": len(result['refined_prompt']['requirements'])
            })
    
    # Summary
    if results:
        print(f"\n\n{'='*80}")
        print("TEST SUITE SUMMARY")
        print(f"{'='*80}")
        print(f"{'Document':<30} {'Valid':<8} {'Complete':<10} {'Reqs'}")
        print(f"{'-'*80}")
        
        for r in results:
            valid_str = "✓" if r['valid'] else "✗"
            comp_str = f"{r['completeness']:.2f}"
            reqs_str = f"{r['requirements']}"
            print(f"{r['document']:<30} {valid_str:<8} {comp_str:<10} {reqs_str}")
        
        print(f"\nTotal Tests: {len(results)}")
        print(f"Valid Prompts: {sum(1 for r in results if r['valid'])}")
        print(f"Avg Requirements: {sum(r['requirements'] for r in results) / len(results):.1f}")


if __name__ == '__main__':
    run_document_tests()
