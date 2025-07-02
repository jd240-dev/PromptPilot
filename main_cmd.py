from agent import call_phi3
from executor import execute_actions

def main():
    while True:
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
            continue
        actions = call_phi3(prompt)
        if actions:
            execute_actions(actions)
        else:
            print("⚠️ No valid actions returned.")

if __name__ == "__main__":
    main()
