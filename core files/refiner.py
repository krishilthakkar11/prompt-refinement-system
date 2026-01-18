"""
Prompt Refiner: LLM-Powered Structured Prompt Generation

Uses GPT-4o with vision capabilities to convert processed inputs
into standardized, validated prompt templates. Performs:
- Intent extraction and problem identification
- Requirement parsing with source attribution
- Constraint and deliverable identification
- Multi-modal conflict detection
- Assumption extraction with risk assessment
- Completeness validation
- Text prompt generation (bonus feature)

Example:
    >>> refiner = PromptRefiner(api_key="sk-...")
    >>> processed = {
    ...     'modalities': ['text'],
    ...     'text_content': [{'source': 'text', 'content': 'Build app'}],
    ...     'image_data': []
    ... }
    >>> result = refiner.refine(processed)
    >>> result['validation']['completeness_score']
    0.73
"""

import json
import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from template import REFINED_PROMPT_TEMPLATE
from validation import PromptValidator

load_dotenv()


class PromptRefiner:
    """
    Core refinement engine using GPT-4o for structured prompt generation.
    
    This class orchestrates the LLM interaction, validation, and text generation.
    It uses a carefully crafted system prompt to guide GPT-4o in extracting
    structured information from multi-modal inputs while maintaining source
    attribution and detecting conflicts.
    
    Design Philosophy:
        - Transparency over assumptions: Never silently fill gaps
        - Flag conflicts with evidence, don't auto-resolve
        - Make all assumptions explicit with risk assessment
        - Maintain source attribution for traceability
    
    Attributes:
        client (OpenAI): OpenAI API client instance
        model (str): Model name (gpt-4o for vision support)
        validator (PromptValidator): Validation engine instance
    
    Example:
        >>> refiner = PromptRefiner(api_key="sk-...")
        >>> processed = processor.process_inputs(inputs)
        >>> result = refiner.refine(processed)
        >>> result['refined_prompt']['intent']['purpose']
        'Create a task management application'
    """
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"  # Supports vision
        self.validator = PromptValidator()
    
    def refine(self, processed_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert processed inputs into validated, structured prompt template.
        
        This is the core refinement method. It:
        1. Builds GPT-4o messages with system prompt and user content
        2. Calls OpenAI API with vision support
        3. Parses JSON response into structured template
        4. Validates completeness using explicit validation rules
        5. Generates human-readable text prompt (bonus feature)
        6. Adds processing metadata
        
        Args:
            processed_inputs (Dict[str, Any]): Output from InputProcessor containing:
                - modalities (list): Input types used
                - text_content (list): Text with source attribution
                - image_data (list): Base64-encoded images
                - notes (list): Processing notes
        
        Returns:
            Dict[str, Any]: Complete refinement result with:
                - refined_prompt (dict): Structured template with:
                    - intent: Purpose, problem, domain, confidence
                    - requirements: Array with text/status/source
                    - constraints: Limitations with impact
                    - deliverables: Expected outputs
                    - conflicts_and_ambiguities: Cross-modal conflicts
                    - assumptions: Explicit assumptions with risk
                - validation (dict):
                    - is_valid_prompt (bool): True if passes validation
                    - rejection_reason (str or None): Why rejected
                    - completeness_score (float): 0.0-1.0 weighted score
                - generated_text_prompt (str or None): Readable version
                - processing_metadata (dict):
                    - input_modalities (list)
                    - notes (list)
        
        Example:
            >>> result = refiner.refine(processed_inputs)
            >>> result['validation']['is_valid_prompt']
            True
            >>> result['validation']['completeness_score']
            0.87
            >>> len(result['refined_prompt']['requirements'])
            8
            >>> result['refined_prompt']['conflicts_and_ambiguities']
            [{'issue': 'Text says BookMyShow but image shows Swiggy', ...}]
        """
        # Build messages for GPT-4
        messages = self._build_messages(processed_inputs)
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,  # Low temperature for consistency
            response_format={"type": "json_object"}
        )
        
        # Parse response
        result = json.loads(response.choices[0].message.content)
        
        # Validate using explicit validation logic
        refined_prompt = result.get('refined_prompt', {})
        validation_result = self.validator.validate(refined_prompt)
        
        # Override validation in result with our explicit validation
        result['validation'] = {
            'is_valid_prompt': validation_result['is_valid_prompt'],
            'rejection_reason': validation_result['rejection_reason'],
            'completeness_score': validation_result['completeness_score']
        }
        
        # Generate clean text prompt from structured data (bonus feature)
        if validation_result['is_valid_prompt']:
            result['generated_text_prompt'] = self._generate_text_prompt(refined_prompt)
        else:
            result['generated_text_prompt'] = None
        
        # Add processing metadata
        result['processing_metadata'] = {
            'input_modalities': processed_inputs['modalities'],
            'notes': processed_inputs.get('notes', [])
        }
        
        return result
    
    def _build_messages(self, processed_inputs: Dict[str, Any]) -> list:
        """Build message array for GPT-4 API call"""
        
        system_prompt = self._get_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add text content
        text_parts = []
        for text_item in processed_inputs['text_content']:
            source = text_item['source']
            content = text_item['content']
            text_parts.append(f"[From {source}]:\n{content}")
        
        # Build user message
        user_content = []
        
        if text_parts:
            user_content.append({
                "type": "text",
                "text": "\n\n".join(text_parts)
            })
        
        # Add images if present
        for image_data in processed_inputs['image_data']:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{image_data['mime_type']};base64,{image_data['base64']}"
                }
            })
        
        # If no content at all, add a placeholder
        if not user_content:
            user_content = [{"type": "text", "text": "No input provided"}]
        
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        return messages
    
    def _get_system_prompt(self) -> str:
        """System prompt that instructs GPT-4 how to refine prompts"""
        
        return f"""You are a prompt refinement system. Your job is to analyze user inputs (text, images, documents) and transform them into a structured, standardized format.

CRITICAL RULES:
1. Never make up information - only extract or reasonably infer from inputs
2. Use status markers correctly:
   - "confirmed": Explicitly stated in input
   - "inferred": Logically derived from context
   - "missing": Not present or unclear
3. Detect and document conflicts between inputs
4. Make assumptions explicit with risk assessment
5. Return ONLY valid JSON matching the template

OUTPUT TEMPLATE STRUCTURE:
{json.dumps(REFINED_PROMPT_TEMPLATE, indent=2)}

GUIDELINES:
- Purpose: What is the user trying to build/achieve?
- Requirements: Extract specific functional needs
- Constraints: Technical, budget, timeline, platform limitations
- Deliverables: What tangible outputs are expected?
- Conflicts: CRITICALLY IMPORTANT - Document ALL contradictions between inputs:
  * Compare text vs image vs document domains
  * Check for conflicting project types (e.g., text says movie booking, image shows food delivery, document describes smart home)
  * Flag conflicting UI patterns (e.g., mobile vs desktop)
  * Note conflicting requirements across sources
  * If text, image, and document all describe different domains/products, this is a MAJOR conflict
- Assumptions: What did you assume that wasn't explicit?

VALIDATION:
- Set is_valid_prompt to false if:
  * No clear product/system intent
  * Purely creative requests (poems, stories, etc.)
  * Completely ambiguous with no actionable information
- Calculate completeness_score (0.0-1.0) based on:
  * Clarity of intent
  * Specificity of requirements
  * Presence of constraints/context

Return ONLY the JSON structure, no other text.
"""
    
    def _generate_text_prompt(self, refined_prompt: dict) -> str:
        """
        Generate a clean, comprehensive text prompt from structured data
        This is a bonus feature showing how structured data can be converted back to text
        
        Args:
            refined_prompt: The structured refined_prompt dict
        
        Returns:
            Clean text prompt suitable for downstream AI systems
        """
        parts = []
        
        # Intent section
        intent = refined_prompt.get('intent', {})
        if intent.get('purpose'):
            parts.append(f"**Objective:** {intent['purpose']}")
        
        if intent.get('problem_being_solved'):
            parts.append(f"\n**Problem Statement:** {intent['problem_being_solved']}")
        
        if intent.get('domain'):
            parts.append(f"\n**Domain:** {intent['domain']}")
        
        # Requirements section
        requirements = refined_prompt.get('requirements', [])
        if requirements:
            parts.append("\n\n**Functional Requirements:**")
            confirmed_reqs = [r for r in requirements if r.get('status') == 'confirmed']
            inferred_reqs = [r for r in requirements if r.get('status') == 'inferred']
            
            if confirmed_reqs:
                parts.append("\n*Explicitly stated:*")
                for i, req in enumerate(confirmed_reqs, 1):
                    parts.append(f"\n{i}. {req['text']}")
            
            if inferred_reqs:
                parts.append("\n\n*Inferred from context:*")
                for i, req in enumerate(inferred_reqs, 1):
                    parts.append(f"\n{i}. {req['text']}")
        
        # Constraints section
        constraints = refined_prompt.get('constraints', [])
        if constraints:
            parts.append("\n\n**Constraints & Limitations:**")
            for i, const in enumerate(constraints, 1):
                parts.append(f"\n{i}. {const['text']}")
                if const.get('impact'):
                    parts.append(f"   - Impact: {const['impact']}")
        
        # Deliverables section
        deliverables = refined_prompt.get('deliverables', [])
        if deliverables:
            parts.append("\n\n**Expected Deliverables:**")
            for i, deliv in enumerate(deliverables, 1):
                parts.append(f"\n{i}. {deliv['item']}")
        
        # Conflicts section (important!)
        conflicts = refined_prompt.get('conflicts_and_ambiguities', [])
        if conflicts:
            parts.append("\n\n**⚠️ Conflicts & Ambiguities to Resolve:**")
            for i, conflict in enumerate(conflicts, 1):
                parts.append(f"\n{i}. {conflict['issue']}")
                if conflict.get('impact'):
                    parts.append(f"   - Impact: {conflict['impact']}")
        
        # Assumptions section
        assumptions = refined_prompt.get('assumptions', [])
        if assumptions:
            parts.append("\n\n**Assumptions Made:**")
            for i, assume in enumerate(assumptions, 1):
                parts.append(f"\n{i}. {assume['assumption']}")
                if assume.get('risk_if_wrong'):
                    parts.append(f"   - Risk if wrong: {assume['risk_if_wrong']}")
        
        return ''.join(parts)
