"""
Content moderation module for safety enforcement.
Students must complete TODO sections according to POLICY.md.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .config import SAFETY_MODE

logger = logging.getLogger(__name__)


class ModerationAction(Enum):
    """Possible moderation actions."""
    ALLOW = "allow"
    BLOCK = "block"
    SAFE_FALLBACK = "safe_fallback"


@dataclass
class ModerationResult:
    """Result of moderation check."""
    action: ModerationAction
    tags: List[str]  # Policy tags that were triggered
    reason: str  # Human-readable explanation
    confidence: float  # Confidence level (0-1)
    fallback_response: Optional[str] = None  # Response to use if action != ALLOW


class Moderator:
    """Handles content moderation according to safety policy."""
    
    def __init__(self):
        """Initialize the moderator with safety rules."""
        self.safety_mode = SAFETY_MODE
        self._initialize_rules()
    
    def _initialize_rules(self):
        """
        Initialize moderation rules based on POLICY.md.
        TODO: Students must define these based on their POLICY.md
        
        IMPLEMENTATION GUIDE:
        1. Copy all keywords and patterns from your completed POLICY.md
        2. Ensure Python formatting (lists, strings, regex compilation)
        3. Templates should be multi-line strings with proper formatting
        """
        
        # TODO: Define crisis keywords and patterns
        # These should detect immediate risk of harm
        self.crisis_keywords = [
            # Direct suicide mentions (examples - add more keywords):
            "suicide", "end my life", "kill myself", "kms", "k1ll", 
            "want to die", "d1e", "death", "leave this world", "take my life", 
            "suicidal", "commit suicide", "ready to die"
        
            # Self-harm expressions (examples - add more keywords):
            "hurt myself", "self-harm", "selfharm", "cut myself", "stab myself", 
            "burn myself", "punish myself",  "harm myself", "slit my wrist",
        
            # Imminent danger indicators (examples - add more keywords):
            "goodbye forever", "final message", "nobody cares", "nobody understands",
            "nothing matters anymore", "hate myself", "hate my life", 
            "life is pointless", "had enough", "cannot go on", "feel alone"

        ]
        
        # TODO: Crisis patterns - regex for complex expressions
        self.crisis_patterns = [
            # Example regex patterns:
            r"\b(want|going|plan|ready|wish) to (die|kill|end)\b",
            r"\b(thinking|thought) about (suicide|dying|ending it)\b",
            r"\b(no reason|point) to live\b",
            r"\b(cut|hurt|harm|burn|kill) (myself)\b",
            r"\b(goodbye|farewell|final) (message|note)\b",
            r"\b(leave|end) (this world|it all)\b",
            r"\b(hate|despise) (myself|my life)\b",
            r"\b(can't|cannot|cant) (go on|take it|handle it)\b",
            r"\b(plan|planning) to (die|kill myself|end my life)\b",
            r"\b(final|last) (goodbye|farewell|message)\b",
            r"\b(feel|feeling) (so )?(alone|hopeless|worthless|trapped|desperate)\b"
            r"\b(wonder|thinking|thought) if (life is worth living|anyone cares)\b"
            # TODO: Add patterns for crisis detection
        ]
        
        # TODO: Define medical request patterns
        self.medical_keywords = [
            # Examples:
            # "diagnose", "what condition",
            # TODO: Add medical request indicators
            # Diagnosis requests
            "diagnose", "diagnosis", "what condition", "check my symptoms", "symptom", "symptoms",
            "evaluate condition", "check for mental disorder", "mental illness",
            
            # Medication & treatment
            "medication", "medicine", "meds", "pills", "antidepressants", 
            "xanax", "sleeping pills", "drug treatment", "prescription", 
            "dosage", "dose", "cure", "treatment", "therapy sessions"
            
            # Mental health terms that could trigger diagnostic queries
            "adhd", "ocd", "ptsd", "phobia", "panic attack", "schizophrenia",
            "anxiety", "depression", "am i depressed", "do i have anxiety"
        ]
        
        # TODO: Medical patterns - regex for complex expressions
        self.medical_patterns = [
            # Example regex patterns:
            # r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
            # TODO: Add patterns for medical detection
            # medication requests
            r"\b(prescribe|recommend|suggest) (medication|pills|drugs)\b",
            r"\bwhat (medication|medicine|pills) should i take\b",
            r"\b(should|can) i (take|use) (antidepressants|xanax|sleeping pills)\b",
            r"\b(recommend|recommended) (dosage|dose) of (medication|antidepressants|xanax|sleeping pills)\b",

            # diagnosis requests
            r"\b(check|diagnose|test) (my symptoms|for mental disorder|for mental illness)\b",
            r"\bdo i have (depression|anxiety|adhd|ocd|ptsd|phobia|panic attack|schizophrenia)\b",
            r"\b(can you|will you) (cure|heal|fix|treat) me\b"
            r"\bwhat (?:disorder|condition|illness) do i have\b"
            r"\bhow (to|do i) (treat|cure) (depression|anxiety|phobia|ptsd|ocd)\b"
        ]
        
        # TODO: Define harmful content patterns
        self.harmful_content = {
            "violence": ["attack", "revenge", "kill", "beat", "punch", 
                         "shoot", "slash", "stab", "bomb", "terrorist", 
                         "massacre", "assault", "torture", "execute", "murder", 
                         "destroy", "hurt"],  # TODO: Violence indicators
            "illegal": ["buy drugs", "sell drugs", "steal", "rob", "theft", 
                        "hacking", "smuggle", "pirate", "illegal", "weapon", 
                        "gun", "drug dealing", "trafficking", "fraud", 
                        "money laundering", "arson", "vandalism"],   # TODO: Illegal activity indicators
            "harassment": ["hate speech", "discriminate", "stigmatise"
                            "bully", "harass", "threaten", "intimidate", 
                            "insult", "abuse", "mock"] # TODO: Harassment indicators
        }
        
        # TODO: Define confidence thresholds based on safety mode
        self.confidence_thresholds = {
            "strict": { 
                "crisis": 0.3,
                "medical": 0.4,
                "harmful": 0.5,
            },
            "balanced": { 
                # TODO: Adjust these
                "crisis": 0.6,
                "medical": 0.6,
                "harmful": 0.7,
            },
            "permissive": { 
                # TODO: Adjust these
                "crisis": 0.8,
                "medical": 0.8,
                "harmful": 0.85,
            }
        }
        
        # TODO: Define safety fallback templates
        # Copy complete templates from POLICY.md
        self.fallback_templates = {
            "crisis": """
I'm deeply concerned about what you're sharing. Safety is my top priority, and I want you to know that help is available right now.

Please reach out to trained crisis counselors immediately (Singapore-specific resources):
- Samaritans of Singapore Limited (SOS): 1767 (24/7)
- National mindline 1771, with 3 ways to reach out to them:
    1. Telephone hotline at 1771;
    2. Mobile messaging service via WhatsApp at +65-6669-1771; and
    3. Online webchat through the chat widget hosted on https://mindline.sg/fsmh

Intense emotions and tough times are difficult to process, and it may feel overwhelming. 
But things can get better. People you trust and trained professionals want to help and will lend a listening ear.

You are not alone, and it’s absolutely alright to seek help. 
            """,
            
            "medical": """
I understand you're looking for medical guidance, and I appreciate you reaching out. 
However, I'm not qualified to provide medical diagnoses or treatment recommendations. 
A licensed medical professional would be the right person who could evaluate what you may need for your situation.

Please reach out to someone who can support you immediately. There are people who care about you and want to help. 

For your health and safety, please consult with:
- A licensed psychiatrist for medication questions
- A therapist for diagnostic assessments and therapy recommendations
- Your primary care physician if you need general consultation over medical conditions


What I can offer you is conversational support, a safe and non-judgemental space to share your thoughts, 
and provide information on how to get to trusted medical help. 
You are not alone, professional help is available and can guide you through the situation you are facing. 
Once you feel ready to do so, please consider booking an appointment with a doctor or medical professional!
            """,

            "harmful": """
I cannot and will not provide assistance with that request as it could potentially cause harm, not only to you, but also to others. 
Your request may have contained mentions of violence, illegal activities, or harassment, which goes against safety policies. 


My main goal is to create a safe space for conversation for you. 
It is valid to experience emotions like anger or frustration, but there are healthy ways to cope with these emotions. 
Would you like to explore some safe strategies, such as stress management or hobbies you like, to manage some of the feelings you are experiencing? 
            """,
            
            "disclaimer": """
Welcome to the Psychological Pre-Consultation Support System, pEAR!

IMPORTANT DISCLAIMER:
This is an AI support system designed to provide initial emotional support and guidance. Please note:
- I cannot provide medical diagnoses or treatment recommendations.
- I am not a substitute for professional mental health care.
- I will not condone any acts of violence, illegal activities, or harassment.
- In cases of crisis or emergency, please contact a qualified professional or helpline immediately.

When to Seek Immediate Help:
If you are in crisis or know someone who is, please seek help from a trained professional and/or contact helplines below.
- Samaritans of Singapore Limited (SOS): 1767 (24/7 Hotline) or 9151 1767 (via WhatsApp)
- National mindline 1771, with 3 ways to reach out to them:
    1. Telephone hotline at 1771;
    2. Mobile messaging service via WhatsApp at +65-6669-1771; and
    3. Online webchat through the chat widget hosted on https://mindline.sg/fsmh

What I Can Offer:
- Conversational support and listening ear to assess your needs
- Safe space that is available 24/7 for you to share your thoughts
- Encouragement to seek help when needed, it is absolutely okay to so so!
- Information on how to get to trusted medical help

Your wellbeing is important. How can I support you today?
            """,
        }
    
    def moderate(
        self,
        user_prompt: str,
        model_response: Optional[str] = None,
        context: Optional[List[Dict]] = None,
    ) -> ModerationResult:
        """
        Perform moderation on user input and/or model output.
        
        Args:
            user_prompt: The user's input text
            
        Returns:
            ModerationResult with action and explanation
            
        IMPLEMENTATION ORDER:
        1. Check crisis (highest priority - must not miss)
        2. Check medical (prevent harmful advice)
        3. Check harmful content (filter inappropriate)
        """
        
        # Example skeleton:
        # Step 1: Check for crisis indicators (highest priority)
        crisis_check = self._check_crisis(user_prompt)
        if crisis_check.action != ModerationAction.ALLOW:
            logger.warning(f"Crisis detected: {crisis_check.reason}")
            return crisis_check
        
        # TODO: Other Steps - Check for ???
        crisis_check = self._check_medical(user_prompt)
        if crisis_check.action != ModerationAction.ALLOW:
            logger.warning(f"Crisis detected: {crisis_check.reason}")
            return crisis_check
        
        crisis_check = self._check_harmful(user_prompt)
        if crisis_check.action != ModerationAction.ALLOW:
            logger.warning(f"Crisis detected: {crisis_check.reason}")
            return crisis_check

        # If model response provided, check it
        if model_response:
            output_check = self._check_model_output(model_response)
            if output_check.action != ModerationAction.ALLOW:
                logger.warning(f"Output violation: {output_check.reason}")
                return output_check
        
        # Check context for concerning patterns
        if context:
            context_check = self._check_context_patterns(context)
            if context_check.action != ModerationAction.ALLOW:
                logger.info(f"Context concern: {context_check.reason}")
                return context_check
        
        # Default: Allow
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Content passes all safety checks",
            confidence=1.0,
        )
    
    def _check_crisis(self, text: str) -> ModerationResult:
        """
        Check for crisis indicators.
        
        TODO: Implement crisis detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. Check against crisis_keywords:
           - If found, set confidence = 0.7
           - Track which keywords were found
        3. Check against crisis_patterns:
           - If matched, set confidence = 0.8-0.9
           - Use re.search() for each pattern
        4. If multiple matches, use MAXIMUM confidence
        5. Get threshold for current safety_mode
        6. If confidence >= threshold:
           - Return BLOCK action
           - Include crisis fallback_response
           - Add descriptive tags
        7. Otherwise return ALLOW
        """

        text_lower = text.lower()
        detected_keywords = []
        detected_patterns = []
        confidence = 0.0

        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
                confidence = max(confidence, 0.7)

        for pattern in self.crisis_patterns:
            if re.search(pattern, text_lower):
                detected_patterns.append(pattern)
                confidence = max(confidence, 0.85)
        
        threshold = self.confidence_thresholds.get(self.safety_mode, {}).get("crisis")

        # 6. If confidence >= threshold, BLOCK
        if confidence >= threshold:
            policy_tags = []
            if detected_keywords:
                policy_tags.append("crisis_keyword")
            if detected_patterns:
                policy_tags.append("crisis_pattern")
            reason = f"I have detected crisis indicators: keywords={detected_keywords}, patterns={detected_patterns}"
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=policy_tags,
                reason=reason,
                confidence=confidence,
                fallback_response=self.fallback_templates.get("crisis", ""),
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No crisis indicators detected",
            confidence=confidence,
        )
    
    def _check_medical(self, text: str) -> ModerationResult:
        """
        Check for medical requests.
        
        TODO: Implement medical request detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. Check against medical_keywords (confidence = 0.7)
        3. Check against medical_patterns (confidence = 0.85)
        4. Use maximum confidence if multiple matches
        5. Compare against threshold for safety_mode
        6. Return SAFE_FALLBACK if threshold exceeded
        
        Note: Use SAFE_FALLBACK, not BLOCK, for medical requests
        """
        text_lower = text.lower()
        detected_keywords = []
        detected_patterns = []
        confidence = 0.0

        for keyword in self.medical_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
                confidence = max(confidence, 0.7)

        for pattern in self.medical_patterns:
            if re.search(pattern, text_lower):
                detected_patterns.append(pattern)
                confidence = max(confidence, 0.85)
        
        threshold = self.confidence_thresholds.get(self.safety_mode, {}).get("medical")
        if confidence >= threshold:
            policy_tags = []
            if detected_keywords:
                policy_tags.append("medical_keyword")
            if detected_patterns:
                policy_tags.append("medical_pattern")
            reason = f"I have detected medical request indicators: keywords={detected_keywords}, patterns={detected_patterns}"
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=policy_tags,
                reason=reason,
                confidence=confidence,
                fallback_response=self.fallback_templates.get("medical", "")
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No medical requests detected",
            confidence=confidence,
        )
    
    def _check_harmful(self, text: str) -> ModerationResult:
        """
        Check for harmful content.
        
        TODO: Implement harmful content detection
        
        ALGORITHM:
        1. Convert text to lowercase
        2. For each category in harmful_content:
           - Check if any keywords present
           - Track which categories triggered
        3. Set confidence = 0.75 for any match
        4. Compare against threshold
        5. Return BLOCK if threshold exceeded
        
        Include triggered categories in tags for debugging
        """

        text_lower = text.lower()
        detected_categories = []
        confidence = 0.0

        for category, keywords in self.harmful_content.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_categories.append(f"Category: {category}, Keyword: {keyword}")
                    confidence = max(confidence, 0.75)

        threshold = self.confidence_thresholds.get(self.safety_mode, {}).get("harmful")
        if confidence >= threshold:
            return ModerationResult(
                action=ModerationAction.BLOCK,
                tags=detected_categories,
                reason=f"Harmful content detected: {detected_categories}",
                confidence=confidence,
                fallback_response=self.fallback_templates.get("harmful", ""))
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="No harmful content detected",
            confidence=confidence,
        )
    
    def _check_model_output(self, response: str) -> ModerationResult:
        """
        Check model output for policy violations.
        
        TODO: Ensure model didn't provide medical advice or break boundaries
        
        ALGORITHM:
        1. Check for medical_keywords that shouldn't appear
        2. Look for diagnosis-like statements
        3. Check for treatment recommendations
        4. Return SAFE_FALLBACK if violations found

        """

        response_lower = response.lower()
        detected_keywords = []
        detected_patterns = []
        confidence = 0.0

        for keyword in self.medical_keywords:
            if keyword in response_lower:
                detected_patterns.append(keyword)
                confidence = max(confidence, 0.4) # lower confidence for output (might include the keywords from clarifications)

        for pattern in self.medical_patterns:
            if re.search(pattern, response_lower):
                detected_patterns.append(pattern)
                confidence = max(confidence, 0.5) # lower confidence for output
        
        threshold = self.confidence_thresholds.get(self.safety_mode, {}).get("medical")
        if confidence >= threshold:
            policy_tags = []
            if detected_keywords:
                policy_tags.append("medical_keyword")
            if detected_patterns:
                policy_tags.append("medical_pattern")
            reason = f"I have detected a medical related response: keywords={detected_keywords}, patterns={detected_patterns}"
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=policy_tags,
                reason=reason,
                confidence=confidence,
                fallback_response=self.fallback_templates.get("medical", "")
            )

        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Model output is appropriate",
            confidence=1.0,
        )
    
    def _check_context_patterns(self, context: List[Dict]) -> ModerationResult:
        
        # Check for escalation
        crisis_count = 0
        for turn in context:
            if turn.get("role") == "user":
                content = turn.get("content", "").lower()
                for keyword in self.crisis_keywords:
                    if keyword in content:
                        crisis_count += 1
        
        if crisis_count >= 3:
            return ModerationResult(
                action=ModerationAction.SAFE_FALLBACK,
                tags=["pattern_escalation", "repeated_crisis"],
                reason="Escalating crisis pattern detected",
                confidence=0.8,
                fallback_response=self.fallback_templates["crisis"],
            )
        
        return ModerationResult(
            action=ModerationAction.ALLOW,
            tags=[],
            reason="Conversation pattern is safe",
            confidence=1.0,
        )
    
    def get_disclaimer(self) -> str:
        """Get initial disclaimer."""
        return self.fallback_templates.get("disclaimer", "")

# Singleton instance
_moderator_instance = None

def get_moderator() -> Moderator:
    """Get singleton moderator instance."""
    global _moderator_instance
    if _moderator_instance is None:
        _moderator_instance = Moderator()
    return _moderator_instance