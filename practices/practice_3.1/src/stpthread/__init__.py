import threading


class StoppableThread(threading.Thread):
    def __init__(self, interface, *args, **kwargs):

        super(StoppableThread, self).__init__(*args, **kwargs)

        self.target = kwargs["target"]
        self.interface = interface

        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.target(self, self.interface)
