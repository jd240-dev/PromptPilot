import atexit
from utils import clear_logs

def init_logger():
    atexit.register(clear_logs)
