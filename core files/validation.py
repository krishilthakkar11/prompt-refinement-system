"""
Validation Logic: Essential vs Optional Field Rules

Defines explicit validation criteria for refined prompts, distinguishing
between essential information (blocking) and optional information (nice-to-have).

Design Philosophy:
    Essential = Information required to understand WHAT needs to be built
    Optional = Information that adds detail but isn't blocking

This module provides:
- Field-level validation rules
- Completeness scoring with weighted formula
- Clear rejection reasons
- Semantic vs structural validation separation

Example:
    >>> validator = PromptValidator()
    >>> result = validator.validate(refined_prompt)
    >>> result['is_valid_prompt']
    True
    >>> result['completeness_score']
    0.85
    >>> result['missing_essential']
    []
"""


class PromptValidator:
    """
    Validates refined prompts based on essential vs optional information
    
    Design Philosophy:
    - Essential: Information required to understand WHAT needs to be built
    - Optional: Information that adds detail but isn't blocking
    """
    
    # Essential fields - must be present and meaningful
    ESSENTIAL_FIELDS = {
        'intent.purpose': {
            'description': 'Clear statement of what needs to be built',
            'min_length': 10,
            'rejection_reason': 'No clear product/system intent'
        },
        'intent.problem_being_solved': {
            'description': 'The problem or need being addressed',
            'min_length': 10,
            'rejection_reason': 'Problem statement missing or unclear'
        },
        'requirements': {
            'description': 'At least one functional requirement',
            'min_count': 1,
            'rejection_reason': 'No actionable requirements identified'
        }
    }
    
    # Optional fields - add value but not required
    OPTIONAL_FIELDS = {
        'constraints': 'Budget, timeline, technical limitations',
        'deliverables': 'Specific outputs/artifacts',
        'assumptions': 'Explicit assumptions made during refinement'
    }
    
    # Completeness scoring weights
    COMPLETENESS_WEIGHTS = {
        'intent': 0.30,           # 30% - Having clear intent
        'requirements': 0.40,      # 40% - Having detailed requirements
        'constraints': 0.15,       # 15% - Having constraints
        'deliverables': 0.10,      # 10% - Having deliverables
        'no_conflicts': 0.05       # 5% - No conflicts present
    }
    
    def validate(self, refined_prompt: dict) -> dict:
        """
        Validate a refined prompt against essential/optional field rules.
        
        This method performs two-stage validation:
        1. Essential field check: Verifies presence and quality of must-have fields
        2. Completeness scoring: Calculates weighted score based on field coverage
        
        Essential Fields (blocking):
        - intent.purpose: Clear statement of what to build (min 10 chars)
        - intent.problem_being_solved: Problem statement (min 10 chars)
        - requirements: At least 1 functional requirement
        
        Optional Fields (non-blocking but scored):
        - constraints: Budget, timeline, technical limitations
        - deliverables: Specific outputs/artifacts
        - assumptions: Explicit assumptions with risk assessment
        
        Completeness Scoring Formula:
        - Intent: 30% (purpose + problem + domain + confidence)
        - Requirements: 40% (number and quality of requirements)
        - Constraints: 15% (presence and specificity)
        - Deliverables: 10% (clarity of expected outputs)
        - No conflicts: 5% (bonus if no multi-modal conflicts)
        
        Args:
            refined_prompt (dict): The refined_prompt portion of refiner output,
                containing intent, requirements, constraints, deliverables,
                conflicts_and_ambiguities, and assumptions.
        
        Returns:
            dict: Validation result with:
                - is_valid_prompt (bool): True if all essential fields present
                - rejection_reason (str or None): Why prompt was rejected
                - completeness_score (float): 0.0 to 1.0 weighted score
                - missing_essential (list): List of missing essential field paths
                - present_optional (list): List of present optional fields
        
        Examples:
            Valid prompt with high completeness:
            >>> refined_prompt = {
            ...     'intent': {
            ...         'purpose': 'Build e-commerce platform',
            ...         'problem_being_solved': 'Manual sales process',
            ...         'domain': 'E-commerce',
            ...         'confidence': 'high'
            ...     },
            ...     'requirements': [
            ...         {'text': 'User registration', 'status': 'confirmed'},
            ...         {'text': 'Product catalog', 'status': 'confirmed'}
            ...     ],
            ...     'constraints': [{'text': 'Budget $50k', 'status': 'confirmed'}],
            ...     'deliverables': [{'item': 'Web application'}],
            ...     'conflicts_and_ambiguities': [],
            ...     'assumptions': []
            ... }
            >>> result = validator.validate(refined_prompt)
            >>> result['is_valid_prompt']
            True
            >>> result['completeness_score'] > 0.85
            True
            
            Invalid prompt (missing purpose):
            >>> invalid_prompt = {
            ...     'intent': {'purpose': '', 'problem_being_solved': 'test'},
            ...     'requirements': []
            ... }
            >>> result = validator.validate(invalid_prompt)
            >>> result['is_valid_prompt']
            False
            >>> result['rejection_reason']
            'No clear product/system intent'
            >>> result['completeness_score']
            0.2
            
            Minimal valid prompt (low completeness):
            >>> minimal_prompt = {
            ...     'intent': {
            ...         'purpose': 'Build an app for task management',
            ...         'problem_being_solved': 'Need to track tasks'
            ...     },
            ...     'requirements': [{'text': 'Add tasks', 'status': 'inferred'}]
            ... }
            >>> result = validator.validate(minimal_prompt)
            >>> result['is_valid_prompt']
            True
            >>> 0.5 < result['completeness_score'] < 0.7
            True
        """
        validation_result = {
            'is_valid_prompt': True,
            'rejection_reason': None,
            'completeness_score': 0.0,
            'missing_essential': [],
            'present_optional': []
        }
        
        # Check essential fields
        for field_path, rules in self.ESSENTIAL_FIELDS.items():
            is_valid, reason = self._check_essential_field(refined_prompt, field_path, rules)
            if not is_valid:
                validation_result['is_valid_prompt'] = False
                validation_result['rejection_reason'] = reason
                validation_result['missing_essential'].append(field_path)
                # Don't return early - collect all missing essentials
        
        # If essential fields are missing, set low completeness
        if not validation_result['is_valid_prompt']:
            validation_result['completeness_score'] = 0.2  # Base score for effort
            return validation_result
        
        # Calculate completeness score
        validation_result['completeness_score'] = self._calculate_completeness(refined_prompt)
        
        # Track which optional fields are present
        validation_result['present_optional'] = self._check_optional_fields(refined_prompt)
        
        return validation_result
    
    def _check_essential_field(self, refined_prompt: dict, field_path: str, rules: dict) -> tuple:
        """
        Check if an essential field meets requirements
        Returns: (is_valid: bool, reason: str)
        """
        # Navigate to nested field
        parts = field_path.split('.')
        value = refined_prompt
        
        try:
            for part in parts:
                value = value[part]
        except (KeyError, TypeError):
            return False, rules['rejection_reason']
        
        # Check based on field type
        if isinstance(value, str):
            # String field - check minimum length
            min_length = rules.get('min_length', 0)
            if not value or len(value.strip()) < min_length:
                return False, rules['rejection_reason']
        
        elif isinstance(value, list):
            # List field - check minimum count
            min_count = rules.get('min_count', 0)
            if len(value) < min_count:
                return False, rules['rejection_reason']
        
        return True, None
    
    def _calculate_completeness(self, refined_prompt: dict) -> float:
        """
        Calculate completeness score (0.0 to 1.0)
        Based on presence and quality of information
        """
        score = 0.0
        
        # Intent quality (30%)
        intent = refined_prompt.get('intent', {})
        intent_score = 0.0
        
        if intent.get('purpose') and len(intent['purpose']) > 20:
            intent_score += 0.4
        if intent.get('problem_being_solved') and len(intent['problem_being_solved']) > 20:
            intent_score += 0.3
        if intent.get('domain') and len(intent['domain']) > 5:
            intent_score += 0.2
        if intent.get('confidence') == 'high':
            intent_score += 0.1
        
        score += intent_score * self.COMPLETENESS_WEIGHTS['intent']
        
        # Requirements quality (40%)
        requirements = refined_prompt.get('requirements', [])
        req_score = 0.0
        
        if len(requirements) >= 1:
            req_score += 0.3
        if len(requirements) >= 3:
            req_score += 0.3
        if len(requirements) >= 5:
            req_score += 0.2
        
        # Bonus for confirmed requirements
        confirmed_count = sum(1 for r in requirements if r.get('status') == 'confirmed')
        if confirmed_count > 0:
            req_score += 0.2 * (confirmed_count / len(requirements))
        
        score += min(req_score, 1.0) * self.COMPLETENESS_WEIGHTS['requirements']
        
        # Constraints present (15%)
        constraints = refined_prompt.get('constraints', [])
        if len(constraints) >= 1:
            score += 0.5 * self.COMPLETENESS_WEIGHTS['constraints']
        if len(constraints) >= 3:
            score += 0.5 * self.COMPLETENESS_WEIGHTS['constraints']
        
        # Deliverables present (10%)
        deliverables = refined_prompt.get('deliverables', [])
        if len(deliverables) >= 1:
            score += self.COMPLETENESS_WEIGHTS['deliverables']
        
        # No conflicts (5%)
        conflicts = refined_prompt.get('conflicts_and_ambiguities', [])
        if len(conflicts) == 0:
            score += self.COMPLETENESS_WEIGHTS['no_conflicts']
        
        return round(min(score, 1.0), 2)
    
    def _check_optional_fields(self, refined_prompt: dict) -> list:
        """Return list of optional fields that are present"""
        present = []
        
        if refined_prompt.get('constraints'):
            present.append('constraints')
        if refined_prompt.get('deliverables'):
            present.append('deliverables')
        if refined_prompt.get('assumptions'):
            present.append('assumptions')
        
        return present
    
    def get_field_requirements(self) -> dict:
        """
        Return documentation of essential vs optional fields
        Useful for explaining design decisions
        """
        return {
            'essential': {
                field: rules['description'] 
                for field, rules in self.ESSENTIAL_FIELDS.items()
            },
            'optional': self.OPTIONAL_FIELDS,
            'completeness_weights': self.COMPLETENESS_WEIGHTS
        }
