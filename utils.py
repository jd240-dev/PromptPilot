import json
import re
import signal
import logging

logger = logging.getLogger("PromptPilot-Utils")

def sanitize_json(text):
    try:
        # Try direct JSON load
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract likely JSON using regex
    try:
        cleaned = re.search(r"\[.*\]", text, re.DOTALL)
        if cleaned:
            raw_json = cleaned.group(0)
            sanitized = re.sub(r"//.*", "", raw_json)  # remove comments
            return json.loads(sanitized)
    except Exception as e:
        logger.error(f"⚠️ Still invalid JSON after cleaning. {e}")
    return []

def timeout_handler(func, timeout_seconds=60):
    def handler(signum, frame):
        raise TimeoutError("Function timed out")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)
    try:
        result = func()
        signal.alarm(0)
        return result
    except Exception as e:
        raise e
