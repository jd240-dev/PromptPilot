import subprocess
import json

def get_command_from_prompt(prompt):
    try:
        result = subprocess.run(
            [
                "ollama", "run", "llama3", f"""
You are a Windows automation assistant.
Convert this prompt into a list of structured actions as JSON:
[
  {{"action": "open", "app": "notepad"}},
  {{"action": "wait", "seconds": 1}},
  {{"action": "type", "text": "hello"}}
]

Prompt: {prompt}
"""],
            capture_output=True,
            text=True,
            timeout=60,  # Increased timeout for slower responses
            encoding="utf-8",
            errors="ignore"
        )

        output = result.stdout.strip()

        # Clean and extract valid JSON block
        try:
            # Sometimes the model adds extra text before/after
            start = output.find('[')
            end = output.rfind(']') + 1
            json_part = output[start:end]
            json.loads(json_part)  # validate
            return json_part
        except Exception as json_err:
            print(f"❌ Invalid JSON from LLaMA:\n{output}")
            return "[]"

    except subprocess.TimeoutExpired:
        print("⏰ LLaMA response timed out after 60 seconds.")
        return "[]"
    except Exception as e:
        print(f"[ERROR llama_agent.py] {e}")
        return "[]"
