import subprocess
import json

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

        # Extract JSON from the model output
        start = output.find('[')
        end = output.rfind(']') + 1
        json_block = output[start:end]

        # Try parsing JSON
        try:
            parsed = json.loads(json_block)
            return json_block
        except json.JSONDecodeError:
            print("⚠️ LLaMA returned invalid JSON. Full output:")
            print(output)
            return "[]"

    except subprocess.TimeoutExpired:
        process.kill()
        print("⏰ phi3 model timed out after 60s.")
        return "[]"
    except Exception as e:
        print(f"🔥 ERROR in llama_agent.py: {e}")
        return "[]"
