import logging
from agent import call_phi3
from executor import execute_action

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)

def main():
    while True:
        prompt = input("Enter your prompt: ").strip()
        if not prompt:
            continue

        actions = call_phi3(prompt)
        if not actions:
            print("⚠️ No valid actions returned.")
            continue

        for action in actions:
            execute_action(action)

if __name__ == "__main__":
    main()
