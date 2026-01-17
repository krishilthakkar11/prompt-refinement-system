"""
Web UI for Prompt Refinement System
Built with Streamlit for easy testing and demonstration
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from main import refine_prompt
import tempfile
import os


# Page config
st.set_page_config(
    page_title="Prompt Refinement System",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-valid {
        color: #28a745;
        font-weight: bold;
    }
    .status-invalid {
        color: #dc3545;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #1f77b4;
    }
    .requirement-item {
        background-color: #f8f9fa;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        border-left: 3px solid #17a2b8;
    }
    .constraint-item {
        background-color: #fff3cd;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        border-left: 3px solid #ffc107;
    }
    .conflict-item {
        background-color: #f8d7da;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        border-left: 3px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)


def display_results(result):
    """Display refined prompt results in a nice format"""
    
    validation = result['validation']
    
    # Validation Status
    st.markdown("---")
    st.markdown("## 📊 Validation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if validation['is_valid_prompt']:
            st.markdown(f"**Status:** <span class='status-valid'>✓ VALID</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Status:** <span class='status-invalid'>✗ INVALID</span>", unsafe_allow_html=True)
            st.error(f"**Rejection Reason:** {validation['rejection_reason']}")
    
    with col2:
        completeness = validation['completeness_score']
        st.metric("Completeness Score", f"{completeness:.2f}", 
                 delta=f"{(completeness - 0.5):.2f}" if completeness > 0.5 else None)
    
    if not validation['is_valid_prompt']:
        return
    
    refined = result['refined_prompt']
    
    # Intent
    st.markdown("---")
    st.markdown("## 🎯 Intent")
    intent = refined['intent']
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Purpose:** {intent['purpose']}")
        st.write(f"**Problem:** {intent['problem_being_solved']}")
        st.write(f"**Domain:** {intent['domain']}")
    with col2:
        confidence_color = {"high": "🟢", "medium": "🟡", "low": "🔴"}
        st.write(f"**Confidence:** {confidence_color.get(intent['confidence'], '⚪')} {intent['confidence'].upper()}")
    
    # Requirements
    if refined['requirements']:
        st.markdown("---")
        st.markdown(f"## 📋 Requirements ({len(refined['requirements'])})")
        
        # Group by source
        sources = {}
        for req in refined['requirements']:
            source = req['source']
            if source not in sources:
                sources[source] = []
            sources[source].append(req)
        
        for source, reqs in sources.items():
            with st.expander(f"From {source.upper()} ({len(reqs)} items)", expanded=True):
                for i, req in enumerate(reqs, 1):
                    status_emoji = {"confirmed": "✅", "inferred": "🔍", "missing": "❓"}
                    st.markdown(f"**{i}.** {req['text']}")
                    st.caption(f"{status_emoji.get(req['status'], '⚪')} Status: {req['status']}")
    
    # Constraints
    if refined['constraints']:
        st.markdown("---")
        st.markdown(f"## ⚠️ Constraints ({len(refined['constraints'])})")
        
        for i, const in enumerate(refined['constraints'], 1):
            with st.container():
                st.markdown(f"**{i}.** {const['text']}")
                st.caption(f"Status: {const['status']} | Impact: {const['impact']}")
    
    # Deliverables
    if refined['deliverables']:
        st.markdown("---")
        st.markdown(f"## 📦 Deliverables ({len(refined['deliverables'])})")
        
        cols = st.columns(min(3, len(refined['deliverables'])))
        for i, deliv in enumerate(refined['deliverables']):
            with cols[i % 3]:
                st.info(f"**{deliv['item']}**\n\nConfidence: {deliv['confidence']}")
    
    # Conflicts
    if refined['conflicts_and_ambiguities']:
        st.markdown("---")
        st.markdown(f"## ⚡ Conflicts & Ambiguities ({len(refined['conflicts_and_ambiguities'])})")
        
        for i, conflict in enumerate(refined['conflicts_and_ambiguities'], 1):
            with st.container():
                st.error(f"**{i}.** {conflict['issue']}")
                st.caption(f"Impact: {conflict['impact']}")
                with st.expander("Evidence"):
                    st.json(conflict['evidence'])
    
    # Assumptions
    if refined['assumptions']:
        st.markdown("---")
        st.markdown(f"## 💭 Assumptions ({len(refined['assumptions'])})")
        
        for i, assume in enumerate(refined['assumptions'], 1):
            with st.container():
                st.markdown(f"**{i}.** {assume['assumption']}")
                st.caption(f"⚠️ Risk if wrong: {assume['risk_if_wrong']}")


def save_result(inputs_description, result):
    """Save result to examples folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f'examples/ui_result_{timestamp}.json')
    output_path.parent.mkdir(exist_ok=True)
    
    output = {
        "timestamp": timestamp,
        "inputs": inputs_description,
        "result": result
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    return output_path


def main():
    """Main Streamlit UI"""
    
    # Header
    st.markdown("<div class='main-header'>🔧 Multi-Modal Prompt Refinement System</div>", unsafe_allow_html=True)
    st.markdown("**Transform diverse inputs (text, images, documents) into structured, standardized prompts**")
    
    # Sidebar for input selection
    st.sidebar.header("Input Configuration")
    st.sidebar.markdown("Select the types of input you want to provide:")
    
    use_text = st.sidebar.checkbox("📝 Text Input", value=True)
    use_image = st.sidebar.checkbox("🖼️ Image Input", value=False)
    use_document = st.sidebar.checkbox("📄 Document Input (PDF/DOCX)", value=False)
    
    # Main input area
    inputs = []
    inputs_description = {}
    
    # Text Input
    if use_text:
        st.header("📝 Text Input")
        st.markdown("Enter your product description, requirements, or idea:")
        
        text_input = st.text_area(
            "Text Description",
            height=200,
            placeholder="Example: Build a mobile app like Uber but for electricians. Users should be able to book electricians, track their arrival, and pay through the app.",
            label_visibility="collapsed"
        )
        
        if text_input.strip():
            inputs.append({'type': 'text', 'content': text_input})
            inputs_description['text'] = text_input[:100] + "..." if len(text_input) > 100 else text_input
    
    # Image Input
    if use_image:
        st.header("🖼️ Image Input")
        st.markdown("Upload an image (wireframe, mockup, sketch, screenshot):")
        
        uploaded_image = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            label_visibility="collapsed"
        )
        
        if uploaded_image is not None:
            # Display the image
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_image.name).suffix) as tmp_file:
                tmp_file.write(uploaded_image.read())
                tmp_path = tmp_file.name
            
            inputs.append({'type': 'image', 'path': tmp_path})
            inputs_description['image'] = uploaded_image.name
    
    # Document Input
    if use_document:
        st.header("📄 Document Input")
        st.markdown("Upload a PDF or DOCX document:")
        
        uploaded_doc = st.file_uploader(
            "Choose a document file",
            type=['pdf', 'docx'],
            label_visibility="collapsed"
        )
        
        if uploaded_doc is not None:
            st.success(f"Uploaded: {uploaded_doc.name}")
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_doc.name).suffix) as tmp_file:
                tmp_file.write(uploaded_doc.read())
                tmp_path = tmp_file.name
            
            inputs.append({'type': 'pdf', 'path': tmp_path})
            inputs_description['document'] = uploaded_doc.name
    
    # Process button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        process_button = st.button("🚀 Refine Prompt", type="primary", use_container_width=True)
    
    # Process inputs
    if process_button:
        if not inputs:
            st.error("⚠️ Please provide at least one input (text, image, or document)")
        else:
            with st.spinner("⏳ Processing your inputs... This may take a moment."):
                try:
                    result = refine_prompt(inputs)
                    
                    # Display results
                    display_results(result)
                    
                    # Save option
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown("### 💾 Save Results")
                    
                    with col2:
                        if st.button("Save to File", use_container_width=True):
                            output_path = save_result(inputs_description, result)
                            st.success(f"✅ Saved to: {output_path}")
                    
                    # Generated Text Prompt (Bonus Feature)
                    if result.get('generated_text_prompt'):
                        st.markdown("---")
                        st.markdown("## 📝 Generated Text Prompt")
                        st.info("✨ **Bonus Feature:** Clean, comprehensive text prompt generated from structured data")
                        with st.expander("View Generated Prompt", expanded=False):
                            st.markdown(result['generated_text_prompt'])
                            
                            # Copy button
                            col1, col2 = st.columns([4, 1])
                            with col2:
                                if st.button("📋 Copy", key="copy_prompt"):
                                    st.success("Copied!")
                    
                    # Show JSON (excluding generated_text_prompt which is shown separately)
                    with st.expander("🔍 View Raw JSON Output"):
                        json_output = {k: v for k, v in result.items() if k != 'generated_text_prompt'}
                        st.json(json_output)
                    
                    # Cleanup temp files
                    for inp in inputs:
                        if 'path' in inp and os.path.exists(inp['path']):
                            try:
                                os.unlink(inp['path'])
                            except:
                                pass
                
                except Exception as e:
                    st.error(f"❌ Error processing inputs: {str(e)}")
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 About")
    st.sidebar.info("""
    This system refines diverse inputs into structured prompts by:
    
    - Extracting intent and requirements
    - Identifying constraints
    - Detecting conflicts
    - Making assumptions explicit
    - Providing completeness scores
    """)
    
    st.sidebar.markdown("### 🎯 Example Use Cases")
    st.sidebar.markdown("""
    - Product requirement docs → Structured specs
    - UI mockups → Feature lists
    - Vague ideas → Actionable requirements
    - Multi-source inputs → Unified prompt
    """)


if __name__ == '__main__':
    main()
