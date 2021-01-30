from datetime import datetime
from termcolor import colored

log_file = 'log.txt'

def log_to_file(val):
  with open(log_file, "a+") as file:
    time_str = colored(datetime.now().strftime('%H-%M-%S'), "blue")
    file.write(f"{time_str} {val}")
    file.write("\n")
