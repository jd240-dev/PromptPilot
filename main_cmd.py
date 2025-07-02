from agent import call_phi3
from executor import execute_actions

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    actions = call_phi3(prompt)
    if actions:
        execute_actions(actions)
    else:
        print("⚠️ No valid actions returned.")
