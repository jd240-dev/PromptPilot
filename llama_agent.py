import subprocess
import json
import re

def clean_json_like(text):
    # Remove comments like // ...
    text = re.sub(r'//.*', '', text)
    return text

def get_command_from_prompt(prompt):
    try:
        process = subprocess.Popen(
            ["ollama", "run", "phi3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        llama_prompt = f"""
You are a Windows automation assistant.
Convert this prompt into a list of structured actions as JSON:
[
  {{"action": "open", "app": "notepad"}},
  {{"action": "wait", "seconds": 1}},
  {{"action": "type", "text": "hello"}}
]

Prompt: {prompt}
"""

        stdout, stderr = process.communicate(input=llama_prompt, timeout=60)
        output = stdout.strip()

        # Extract JSON block
        start = output.find('[')
        end = output.rfind(']') + 1
        json_block = output[start:end]

        # Clean JSON block of comments
        json_block = clean_json_like(json_block)

        try:
            json.loads(json_block)  # Validate JSON
            return json_block
        except json.JSONDecodeError:
            print("⚠️ Still invalid JSON after cleaning. Full output:")
            print(output)
            return "[]"

    except subprocess.TimeoutExpired:
        process.kill()
        print("⏰ phi3 model timed out after 60s.")
        return "[]"
    except Exception as e:
        print(f"🔥 ERROR in llama_agent.py: {e}")
        return "[]"
