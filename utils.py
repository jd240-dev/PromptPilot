# utils.py

import json
import re

def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except Exception:
        return False

def extract_json(text):
    try:
        # Extract JSON-like content from text using regex
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if match:
            return match.group(0)
    except Exception:
        return None
    return None

def log(message, level="INFO"):
    print(f"[{level}] {message}")
