from agent import call_phi3
from executor import execute_all
from logger import init_logger
from utils import log_action

init_logger()

prompt = input("Enter your prompt: ")
actions = call_phi3(prompt)
log_action(prompt, actions)
execute_all(actions)
