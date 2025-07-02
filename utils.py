import re

def clean_json(text: str) -> str:
    """
    Extracts and sanitizes the first valid JSON list from model output.
    Strips comments, code block markers, and invalid blocks.
    """
    # Remove code block markers (```json ... ```)
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "")
    
    # Remove lines with obvious syntax errors or non-JSON content
    lines = text.splitlines()
    json_lines = [line for line in lines if ":" in line and not line.strip().startswith("//")]

    cleaned_text = "\n".join(json_lines)
    
    # Attempt to extract the first valid JSON list
    match = re.search(r"\[\s*{.*?}\s*\]", cleaned_text, re.DOTALL)
    if match:
        return match.group(0)
    return "[]"
