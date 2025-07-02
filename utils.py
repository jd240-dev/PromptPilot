import re
import json

def clean_json(text: str) -> str:
    """
    Extract and sanitize the first valid JSON array of actions from model output.
    Handles extra text, invalid characters, and nested garbage gracefully.
    """
    # Remove code block formatting
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "").strip()

    # Remove any trailing commas before a closing brace/bracket (which break JSON)
    text = re.sub(r",(\s*[}\]])", r"\1", text)

    # Try to locate the first JSON array
    potential_arrays = re.findall(r"\[\s*{.*?}\s*]", text, re.DOTALL)

    for block in potential_arrays:
        try:
            # Try parsing the block to see if it's valid JSON
            parsed = json.loads(block)
            if isinstance(parsed, list) and all(isinstance(p, dict) and "action" in p for p in parsed):
                return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            continue

    # Fallback: return empty valid JSON array if nothing found
    return "[]"

def print_colored(text: str, color: str = "yellow") -> None:
    """
    Print colored text to the terminal using ANSI escape codes.
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")
