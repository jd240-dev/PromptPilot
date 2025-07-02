import json
import logging
import threading
import time

logger = logging.getLogger("PromptPilot-Agent")

def sanitize_json(response: str):
    try:
        json_start = response.index('[')
        json_str = response[json_start:]
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"❌ JSON parsing failed: {e}")
        return None

def run_with_timeout(func, args=(), kwargs=None, timeout_duration=15):
    result = [None]
    kwargs = kwargs or {}

    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            result[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout_duration)

    if thread.is_alive():
        logger.error("❌ ERROR: Phi3 model response timed out.")
        return None

    return result[0]

def timeout_handler(signum, frame):
    raise TimeoutError("Phi3 model response timed out.")
