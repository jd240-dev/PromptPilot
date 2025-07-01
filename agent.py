import subprocess
import json
import re
import logging
from utils import clean_text

logger = logging.getLogger("PromptPilot")

def call_llm(prompt):
    try:
        full_prompt = (
            "You are a Windows automation assistant.\n"
            "Convert the following instruction into a list of JSON actions. Only return JSON, nothing else.\n\n"
            "Instruction:\n" + prompt
        )

        result = subprocess.run(
            ["ollama", "run", "phi3", full_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        output = result.stdout.strip()
        logger.info("🔧 Raw model output:\n%s", output)

        return parse_actions(output)

    except subprocess.TimeoutExpired:
        logger.error("❌ LLM response timed out.")
        return []
    except Exception as e:
        logger.exception("❌ Unexpected error calling LLM: %s", e)
        return []

def parse_actions(raw_output):
    try:
        # Strip code block markers like ```json or ```
        cleaned_output = re.sub(r"```(json)?", "", raw_output, flags=re.IGNORECASE).strip()
        cleaned_output = re.sub(r"```", "", cleaned_output).strip()

        # Remove single-line comments if any
        cleaned_output = re.sub(r'//.*', '', cleaned_output)

        # If multiple JSON-like objects, pick first valid array
        matches = re.findall(r'\[\s*{.*?}\s*\]', cleaned_output, re.DOTALL)
        if not matches:
            raise ValueError("No JSON array found.")

        for match in matches:
            try:
                actions = json.loads(match)
                if isinstance(actions, list):
                    return actions
            except json.JSONDecodeError:
                continue

        raise ValueError("All extracted JSON arrays are invalid.")

    except Exception as e:
        logger.error("❌ JSON parsing failed: %s", e)
        logger.debug("⚠️ Still invalid JSON after cleaning. Full output:\n%s", raw_output)
        return []
