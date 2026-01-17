# Multi-Modal Prompt Refinement System

A system that transforms diverse inputs (text, images, documents) into structured, standardized prompts using GPT-4o. Built as an internship assignment for Dignifiedme Technologies.

## 🎯 Features

- **Multi-Modal Input Processing**: Text, images (PNG/JPG), and documents (PDF/DOCX)
- **Structured Output Template**: Consistent JSON format with intent, requirements, constraints, and deliverables
- **Conflict Detection**: Identifies contradictions across different input sources
- **Completeness Scoring**: Weighted validation system for prompt quality
- **Interactive Web UI**: Streamlit-based interface for easy testing
- **Generated Text Prompts**: Bonus feature converting structured data to readable text

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/prompt-refinement-system.git
   cd prompt-refinement-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-key-here
   ```

### Running the Application

#### Option A: Web UI (Recommended)
```bash
python -m streamlit run app.py
```
Then open your browser to http://localhost:8501

#### Option B: Command-Line Examples
```bash
python main.py
```

#### Option C: Test Suites
```bash
# Test text inputs
python test_text_inputs.py

# Test image inputs
python test_image_inputs.py

# Test multi-modal inputs
python test_multimodal.py

# Test document inputs
python test_document_inputs.py
```

## 📖 Usage

### Programmatic Usage

```python
from main import refine_prompt

# Text only
result = refine_prompt([
    {"type": "text", "content": "Build an e-commerce app for handmade crafts"}
])

# Multi-modal: Text + Image
result = refine_prompt([
    {"type": "text", "content": "Create a food delivery app"},
    {"type": "image", "path": "ui_mockup.png"}
])

# With document
result = refine_prompt([
    {"type": "document", "path": "requirements.pdf"}
])

# Access results
print(f"Valid: {result['validation']['is_valid_prompt']}")
print(f"Completeness: {result['validation']['completeness_score']}")
print(f"Requirements: {len(result['refined_prompt']['requirements'])}")
```

## 🏗️ Project Structure

```
├── main.py                      # Main entry point and refine_prompt() function
├── refiner.py                   # Core refinement engine using GPT-4o
├── input_processor.py           # Multi-modal input processing
├── validation.py                # Prompt validation and scoring
├── template.py                  # Output template structure
├── app.py                       # Streamlit web interface
├── requirements.txt             # Python dependencies
├── .env.example                 # API key template
│
├── docs/
│   ├── essential_vs_optional.md # Design decisions documentation
│   └── template_design.md       # Template justification (TODO)
│
├── examples/                    # Sample inputs and outputs
├── test_images/                 # Test image files
├── test_documents/              # Test document files
│
└── test_*.py                    # Test suites
```

## 📊 Output Structure

The system produces a structured JSON output with:

- **Intent**: Purpose, problem being solved, domain, confidence level
- **Requirements**: Extracted functional needs (confirmed/inferred/missing)
- **Constraints**: Technical, budget, timeline limitations with impact assessment
- **Deliverables**: Expected outputs
- **Conflicts**: Contradictions between input sources with evidence
- **Assumptions**: Explicit assumptions with risk assessment
- **Validation**: Completeness score and validity status
- **Generated Text Prompt**: Human-readable text version (bonus feature)

## 🎨 Examples

See the [examples/](examples/) directory for sample inputs and outputs covering:
1. Detailed/complete prompts (high completeness)
2. Minimal/vague inputs (low completeness)
3. Multi-modal with conflicts
4. Document-based inputs
5. Edge cases

## 🧠 Design Philosophy

- **Transparency over assumptions**: Never silently fill gaps
- **Conflict flagging**: Document contradictions, don't auto-resolve
- **Source attribution**: Track where each requirement came from
- **Explicit validation**: Clear rules for essential vs. optional fields

See [docs/essential_vs_optional.md](docs/essential_vs_optional.md) for detailed design decisions.

## 📝 License

This project was created as an internship assignment for Dignifiedme Technologies.

## 👤 Author

[Your Name]
Internship Assignment - January 2026
