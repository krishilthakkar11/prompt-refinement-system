"""
Refined Prompt Template Structure
This is the target output format for all refined prompts.
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
