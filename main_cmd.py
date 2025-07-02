import logging
from agent import call_phi3
from executor import execute_actions

logging.basicConfig(level=logging.INFO)

def main():
    while True:
        prompt = input("Enter your prompt: ")
        if prompt.lower() in ["exit", "quit"]:
            break

        actions = call_phi3(prompt)
        if actions:
            execute_actions(actions)
        else:
            print("⚠️ No valid actions returned.")

if __name__ == "__main__":
    main()
