import threading
import Pyro4


class NameServer:
    def __init__(self):
        self.name_server_daemon = None

    def run(self):
        nsUri, daemon, bcserver = Pyro4.naming.startNS()
        self.name_server_daemon = daemon
        print nsUri, daemon, bcserver
        try:
            daemon.requestLoop()
        except Exception:
            import traceback
            traceback.print_exc()
        finally:
            daemon.close()
            if bcserver is not None:
                bcserver.close()
        print("NS shut down.")

    def shutdown(self):
        self.name_server_daemon.shutdown()

if __name__ == '__main__':
    n = NameServer()
    n.run()