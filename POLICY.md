# Safety and Moderation Policy

## Overview

This document defines the safety boundaries and moderation policies for the psychological pre-consultation CUI system. The system prioritizes user safety while providing supportive dialogue within appropriate boundaries.

## Policy Framework

### 1. Safety Categories

#### 1.1 Crisis Situations

**Definition**: Immediate risk of harm to self or others

**Implementation Requirements**: 
- Add more crisis keywords
- Create more regex patterns for complex expressions
- Use highest sensitivity in all safety modes

```python
CRISIS_KEYWORDS = [
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

# Regex patterns for complex expressions
CRISIS_PATTERNS = [
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
]
```

**Action**: `BLOCK` + Crisis referral

**Example Response Template (Complete this with 150-200 words)**: 

```text
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
```

#### 1.2 Medical Requests

**Definition**: Requests for diagnosis, treatment, or medication advice

**Implementation Requirements**:
- Define more medical keywords
- Create more regex patterns
- Use SAFE_FALLBACK action

```python
MEDICAL_INDICATORS = [
    # Diagnosis requests (add more keywords):
    "diagnose", "diagnosis", "what condition", "check my symptoms", "symptom", "symptoms",
    "evaluate condition", "check for mental disorder", "mental illness",
    
    # Medication/treatment (add more keywords):
    "medication", "medicine", "meds", "pills", "antidepressants", 
    "xanax", "sleeping pills", "drug treatment", "prescription", 
    "dosage", "dose", "cure", "treatment", "therapy sessions"
    
    # Mental health specific (add more keywords):
    "adhd", "ocd", "ptsd", "phobia", "panic attack", "schizophrenia",
    "anxiety", "depression", "am i depressed", "do i have anxiety", "bipolar"
]

# Minimum 8 regex patterns for complex expressions
MEDICAL_PATTERNS = [
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
```

**Action**: `SAFE_FALLBACK`

**Response Template (Complete with structured format)**: 

```text
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
```

#### 1.3 Harmful Content

**Definition**: Violence, illegal activities, harassment

**Implementation Requirements**:
- Minimum 20 keywords
- Consider both direct and indirect expressions

```python
HARMFUL_CATEGORIES = {
    "violence": ["attack", "revenge", "kill", "beat", "punch", 
                    "shoot", "slash", "stab", "bomb", "terrorist", 
                    "massacre", "assault", "torture", "execute", "murder", 
                    "destroy", "hurt"], 
    "illegal": ["buy drugs", "sell drugs", "steal", "rob", "theft", 
                "hacking", "smuggle", "pirate", "illegal", "weapon", 
                "gun", "drug dealing", "trafficking", "fraud", 
                "money laundering", "arson", "vandalism"],  
    "harassment": ["hate speech", "discriminate", "stigmatise"
                    "bully", "harass", "threaten", "intimidate", 
                    "insult", "abuse", "mock"]
}
```

**Action**: `BLOCK`

**Example Response Template (Complete this with 150-200 words)**: 

```text
I cannot and will not provide assistance with that request as it could potentially cause harm, not only to you, but also to others. 
Your request may have contained mentions of violence, illegal activities, or harassment, which goes against safety policies. 

My main goal is to create a safe space for conversation for you. 
It is valid to experience emotions like anger or frustration, but there are healthy ways to cope with these emotions. 
Would you like to explore some safe strategies, such as stress management or hobbies you like, to manage some of the feelings you are experiencing? 
```

#### 1.4 Supportive Dialogue

**Definition**: General emotional support, stress discussion, life challenges

**Acceptable Topics** (define at least 10):
```python
SUPPORTIVE_TOPICS = [
    "stress management",
    "relationship challenges",
    "work-life balance",
    "anxiety coping",
    "grief and loss",
    "time management",
    "academic stress",
    "self-esteem",
    "personal growth",
    "hobbies",
    "future aspirations",
    "goals"
]
```

**Action**: `ALLOW`

### 2. Action Definitions

- **ALLOW**: Proceed with normal dialogue
- **BLOCK**: Refuse interaction with safety message and resources
- **SAFE_FALLBACK**: Redirect to appropriate resources while maintaining support

### 3. Confidence and Ambiguity

**Confidence Score Guidelines**:
- Keyword match: 0.7 confidence
- Pattern match: 0.8-0.9 confidence
- Multiple matches: Use maximum confidence

**Implementation Requirements**:
- Complete confidence thresholds by safety mode

**Confidence Thresholds by Safety Mode**:

```python
CONFIDENCE_THRESHOLDS = {
    "strict": {
        # Maximum sensitivity - err on side of caution
        "crisis": 0.3,   # Very low threshold for crisis detection
        "medical": 0.4,  # Low threshold for medical boundaries
        "harmful": 0.5   # Moderate threshold for harmful content
    },
    "balanced": {
        # Balanced approach for production use
        # prioritise user's personal safety, hence crisis and medical threshold is a little lower
        "crisis": 0.6,   # Moderate threshold for crisis detetion
        "medical": 0.6,  # Moderate  threshold for crisis detetion
        "harmful": 0.7,  # Moderate to high threshold for crisis detetion - only strong messages will be flagged
    },
    "permissive": {
        # Minimum filtering - only clear violations
        "crisis": 0.8,
        "medical": 0.8,
        "harmful": 0.85,
    }
}
```

### 5. Response Templates

**Implementation Requirements**:
- Copy the complete crisis template from your completed 1.1 Crisis Situations above.
- Copy the complete medical template from your completed 1.2 Medical Requests above.
- Copy the complete harmful template from your completed 1.3 Harmful Content above.
- Complete disclaimer template.

```python
RESPONSE_TEMPLATES = {
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
    """
}
```
