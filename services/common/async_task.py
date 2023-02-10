import threading
from typing import Callable


class AsyncTask:
    def __init__(self, fn: Callable, *args, **kwargs):
        self.fn = fn
        self.t = threading.Thread(target=self._run, args=args, kwargs=kwargs)
        self.t.daemon = True
        self.t.start()

    def _run(self, *args, **kwargs):
        try:
            self.res = self.fn(*args, **kwargs)
        except Exception as ex:
            self.error = ex
            pass
