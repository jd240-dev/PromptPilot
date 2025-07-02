import json
import re
import logging
import threading

logger = logging.getLogger("PromptPilot-Utils")

def sanitize_json(raw_output):
    try:
        json_str = extract_json_like_block(raw_output)
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parsing failed - {e}")
        return []
    except Exception as e:
        logger.error(f"❌ JSON sanitization error: {e}")
        return []

def extract_json_like_block(text):
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("No valid JSON block found.")

def run_with_timeout(func, timeout):
    result = {}
    def wrapper():
        try:
            result["value"] = func()
        except Exception as e:
            result["error"] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutError("Function timed out.")
    if "error" in result:
        raise result["error"]
    return result.get("value")
