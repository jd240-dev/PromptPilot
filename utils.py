import json
import re
import logging
import threading

logger = logging.getLogger("PromptPilot-Utils")

def sanitize_json(response: str):
    try:
        json_start = response.index('[')
        json_end = response.rindex(']') + 1
        cleaned_json = response[json_start:json_end]
        # Remove trailing commas or invalid JSON parts
        cleaned_json = re.sub(r",\s*([}\]])", r"\1", cleaned_json)
        parsed = json.loads(cleaned_json)
        return parsed
    except Exception as e:
        logger.error(f"❌ Error in sanitize_json: {e}")
        raise

def run_with_timeout(func, args=(), kwargs={}, timeout_duration=10):
    result = [None]
    exception = [None]

    def wrapper():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout_duration)

    if thread.is_alive():
        return TimeoutError("Function timed out.")
    if exception[0]:
        return exception[0]

    return result[0]
