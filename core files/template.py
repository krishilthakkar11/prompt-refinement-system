"""
Refined Prompt Template Structure

This module defines the standardized JSON schema for all refined prompts.
It serves as the target output format for the refinement system, ensuring
consistency and completeness across all outputs.

Template Design Philosophy:
    1. Transparency: Never hide gaps or uncertainties
    2. Source Attribution: Track which modality (text/image/document) 
       contributed each piece of information
    3. Conflict Detection: Flag contradictions with evidence
    4. Explicit Assumptions: Document what was inferred vs confirmed
    5. Risk Assessment: Identify potential risks if assumptions are wrong

Key Sections:
    - intent: Core purpose and problem identification
    - requirements: Functional and non-functional requirements with status
    - constraints: Limitations with impact assessment
    - deliverables: Expected outputs with confidence
    - conflicts_and_ambiguities: Cross-modal conflicts with evidence
    - assumptions: Explicit assumptions with risk if wrong
    - validation: Completeness and validity metrics
    - processing_metadata: Input modalities and notes

For detailed design rationale, see docs/template_design.md

Example:
    >>> from template import REFINED_PROMPT_TEMPLATE
    >>> import json
    >>> print(json.dumps(REFINED_PROMPT_TEMPLATE, indent=2))
"""

REFINED_PROMPT_TEMPLATE = {
    "refined_prompt": {
        "intent": {
            "purpose": "",
            "problem_being_solved": "",
            "domain": "",
            "confidence": "high | medium | low"
        },
        "requirements": [
            {
                "text": "",
                "status": "confirmed | inferred | missing",
                "source": "text | image | document"
            }
        ],
        "constraints": [
            {
                "text": "",
                "status": "confirmed | inferred",
                "impact": ""
            }
        ],
        "deliverables": [
            {
                "item": "",
                "confidence": "high | medium | low"
            }
        ],
        "conflicts_and_ambiguities": [
            {
                "issue": "",
                "evidence": {},
                "impact": ""
            }
        ],
        "assumptions": [
            {
                "assumption": "",
                "risk_if_wrong": ""
            }
        ]
    },
    "validation": {
        "is_valid_prompt": True,
        "rejection_reason": None,
        "completeness_score": 0.0
    },
    "processing_metadata": {
        "input_modalities": [],
        "notes": []
    }
}
