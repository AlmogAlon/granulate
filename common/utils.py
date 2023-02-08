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


class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated
        self._instance = None

    @property
    def instance(self):
        if not self._instance:
            self._instance = self._decorated()
        return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')
