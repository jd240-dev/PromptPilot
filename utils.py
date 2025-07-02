import json
import re
import threading
import subprocess
import logging

logger = logging.getLogger("PromptPilot-Utils")

def sanitize_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    try:
        cleaned = re.search(r"\[.*\]", text, re.DOTALL)
        if cleaned:
            raw_json = cleaned.group(0)
            sanitized = re.sub(r"//.*", "", raw_json)
            return json.loads(sanitized)
    except Exception as e:
        logger.error(f"⚠️ Still invalid JSON after cleaning. {e}")
    return []

def run_with_timeout(func, timeout_seconds=60):
    result = {}
    exception = {}

    def wrapper():
        try:
            result['value'] = func()
        except Exception as e:
            exception['error'] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout_seconds)

    if thread.is_alive():
        raise subprocess.TimeoutExpired(cmd='ollama run', timeout=timeout_seconds)
    if 'error' in exception:
        raise exception['error']
    return result.get('value')
