import threading

class module(threading.Thread):

    cmd = ".hello"

    def __init__(self, msg, queue):
        super(module, self).__init__()
        self.msg = msg
        self.queue = queue

    def run(self):
        self.msg["MSG"] = "Yay modules!!"
        self.queue.put(self.msg)
        return
