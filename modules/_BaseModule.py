import http
import inspect
import threading
import traceback

class BaseModule(threading.Thread):

    def __init__(self, msg, queue):
        super(BaseModule, self).__init__()
        self.msg = msg
        self.queue = queue
        
    # Main entrypoint for thread, override this
    def main(self):
        raise NotImplementedError

    # Do not override! Allows bot to inform sender a module has crashed
    def run(self):
        try:
            self.main()
        except:
            mem = inspect.getmembers(self)
            name = [n[1] for n in mem if n[0] == "__class__"][0]
            self.sendmsg("Thread {} has crashed!"
                    .format(name))
            print(traceback.print_exc())

    # Send a message to where the message came from (either user/channel)
    def sendmsg(self, string):
        self.queue.put({"TO":self.msg["TO"], "FROM":self.msg["FROM"],
                        "MSG":string})

    # Send a PM to the user who triggered the command
    def sendpm(self, string):
        self.queue.put({"TO":"", "FROM":self.msg["FROM"],
                        "MSG":string})

    # Send a message to the specified target (user/channel)
    def sendto(self, target, string):
        self.queue.put({"TO":target, "FROM":self.msg["FROM"],
                        "MSG":string})
    
    # Request a page and return either RESPONSE or actual HTML
    def _requestPage(self, conn, method, url, body, header, resptype):
        try:
            conn.request(method, url, body, header)
            resp = conn.getresponse()
            conn.close()
            if resptype == 0:
                return resp
            elif resptype == 1:
                return resp.read().decode("utf-8")
        except:
            return None

    # Request a HTML page from the connection and return the RESPONSE
    def reqPage(self, conn, method, url, body, header):
        return self._requestPage(conn, method, url, body, header, 0)
    
    # Request a HTML page from the connection and return the HTML
    def reqHTML(self, conn, method, url, body, header):
        return self._requestPage(conn, method, url, body, header, 1)
        