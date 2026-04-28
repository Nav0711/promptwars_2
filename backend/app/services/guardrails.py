import re

class GuardrailException(Exception):
    pass

def check_input_guardrails(user_input: str) -> bool:
    """
    Pre-query classifier to detect political opinions or predictions.
    Returns True if the query is blocked by a guardrail.
    """
    # Hard-blocked topics
    blocked_patterns = [
        r"who will win",
        r"predict result",
        r"exit poll",
        r"best party",
        r"worst candidate",
        r"should (i|we) vote for",
        r"is \w+ corrupt",
    ]
    
    # Prompt injection patterns
    injection_patterns = [
        r"ignore previous instructions",
        r"you are now",
        r"system prompt",
        r"jailbreak",
        r"dan mode"
    ]
    
    lower_input = user_input.lower()
    
    for pattern in blocked_patterns + injection_patterns:
        if re.search(pattern, lower_input):
            return True
            
    return False

def get_guardrail_message(user_input: str) -> str:
    """
    Returns the appropriate message for a blocked query.
    """
    lower_input = user_input.lower()
    if "predict" in lower_input or "win" in lower_input or "exit poll" in lower_input:
        return "I don't make predictions about election outcomes. I can share official schedules and historical data instead."
    else:
        return "I'm here to share factual election information only. I don't share opinions on political parties or candidates."
