import re
import json
import logging

logger = logging.getLogger("PromptPilot-Utils")

def clean_text(text: str) -> str:
    """
    Strips leading/trailing whitespace and removes invalid characters.
    """
    return text.strip().replace('\x00', '').replace('\u0000', '')


def sanitize_json(text: str) -> str:
    """
    Cleans and attempts to fix malformed JSON output from the model.
    Handles:
    - Improper quotes
    - Trailing commas
    - Multiple JSON blocks
    - Code block wrappers
    """
    # Remove triple backticks or language markers like ```json
    text = re.sub(r"```(json)?", "", text).strip("` \n")

    # Try to extract JSON array or object
    json_match = re.search(r'(\[\s*{.*?}\s*\])', text, re.DOTALL)
    if not json_match:
        json_match = re.search(r'({.*})', text, re.DOTALL)

    if json_match:
        cleaned = json_match.group(1)
    else:
        cleaned = text

    # Fix common JSON issues
    cleaned = re.sub(r",\s*}", "}", cleaned)
    cleaned = re.sub(r",\s*]", "]", cleaned)

    # Ensure valid double quotes
    cleaned = re.sub(r"‘|’|“|”", "\"", cleaned)

    # Remove trailing commas
    cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)

    # Fix incorrect quotes around keys
    cleaned = re.sub(r"([,{]\s*)([a-zA-Z0-9_]+)(\s*:\s*)", r'\1"\2"\3', cleaned)

    # Remove any non-JSON trailing data
    try:
        # Final validation
        json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.warning(f"⚠️ JSON still may be invalid: {e}")

    return cleaned
