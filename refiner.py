"""
Prompt Refiner: Uses GPT-4 to convert processed inputs into structured template
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
    """Refines processed inputs into structured prompt format"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"  # Supports vision
        self.validator = PromptValidator()
    
    def refine(self, processed_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Take processed inputs and generate refined prompt structure
        
        Args:
            processed_inputs: Output from InputProcessor.process_inputs()
        
        Returns:
            Refined prompt following the template structure
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
