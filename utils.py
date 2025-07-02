import subprocess
import json
import re
from logger import setup_logger

logger = setup_logger("PromptPilot-Utils")

def sanitize_json(raw_output: str):
    try:
        # Remove markdown code block
        raw_output = raw_output.strip("` \njson")
        # Extract first valid JSON array
        matches = re.findall(r'\[\s*{.*?}\s*\]', raw_output, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        logger.warning("⚠️ No valid JSON arrays found.")
    except Exception as e:
        logger.error(f"❌ JSON sanitization failed: {e}")
    return []

def timeout_subprocess(cmd, timeout=60):
    result = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True)
    return result.stdout
