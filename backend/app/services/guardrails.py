"""
guardrails.py — Multi-layer guardrail system for Chunav Saathi.
Covers English AND Hindi patterns for political sensitivity.
"""
import re

class GuardrailException(Exception):
    pass

# Hard-blocked topics
_BLOCKED_EN = [
    r"who (will|should|would) win",
    r"predict(ion)? (the )?result",
    r"exit poll",
    r"best party",
    r"worst (party|candidate|politician|leader)",
    r"should (i|we|you) vote for",
    r"is \w+ corrupt",
    r"vote for (bjp|congress|aap|sp|bsp|tnc|tmc|shiv sena)",
    r"which party (is|will be) better",
]

# Hindi phonetic/romanized blocked patterns
_BLOCKED_HI = [
    r"kaun jeet(ega|a)",       # who will win
    r"kise vote (dun|du|den)", # whom to vote
    r"sabse acha (party|neta|dal)",  # best party/leader
    r"sabse bura (party|neta|dal)",  # worst party/leader
    r"result kya hoga",         # what will be the result
]

# Prompt injection patterns
_INJECTION = [
    r"ignore (previous|all|your) instruction",
    r"you are now",
    r"new persona",
    r"system prompt",
    r"jailbreak",
    r"dan mode",
    r"act as (a |an )?different",
    r"forget (your|all) (rules|instructions)",
]

ALL_PATTERNS = _BLOCKED_EN + _BLOCKED_HI + _INJECTION


def check_input_guardrails(user_input: str) -> bool:
    """
    Returns True if the query should be blocked.
    """
    lower = user_input.lower().strip()
    # Hard cap on length to prevent token abuse
    if len(lower) > 1500:
        return True
    for pattern in ALL_PATTERNS:
        if re.search(pattern, lower):
            return True
    return False


def get_guardrail_message(user_input: str, language: str = "en") -> str:
    """
    Returns an appropriate polite decline message.
    Bilingual: Hindi if language == 'hi'.
    """
    lower = user_input.lower()
    is_prediction = any(kw in lower for kw in [
        "predict", "win", "exit poll", "jeet", "result kya hoga"
    ])
    is_injection = any(kw in lower for kw in [
        "ignore", "jailbreak", "dan mode", "system prompt", "you are now"
    ])

    if language == "hi":
        if is_prediction:
            return "मैं चुनाव परिणामों के बारे में भविष्यवाणी नहीं करता। मैं आपको आधिकारिक चुनाव कार्यक्रम और ऐतिहासिक डेटा दे सकता हूँ।"
        return "मैं केवल तथ्यात्मक चुनाव जानकारी साझा करता हूँ। राजनीतिक दलों या उम्मीदवारों पर कोई राय व्यक्त करना मेरे लिए संभव नहीं है।"

    if is_injection:
        return "I can only answer questions about Indian elections. Please ask me about election schedules, voter registration, or polling booths."
    if is_prediction:
        return "I don't make predictions about election outcomes. I can share official schedules and historical data instead."
    return "I'm here to share factual election information only. I don't share opinions on political parties or candidates."
