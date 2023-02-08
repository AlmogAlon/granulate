import logging
import sys


def initialize_logging_to_stdout(level=logging.DEBUG):
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    root.addHandler(ch)


def pluck(obj, pluck_list):
    return {key: obj[key] for key in pluck_list if key in obj}
