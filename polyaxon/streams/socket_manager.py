class SocketManager(object):
    def __init__(self):
        self.ws = set()

    def add_socket(self, ws):
        self.ws.add(ws)

    def remove_sockets(self, disconnected_ws):
        if not isinstance(disconnected_ws, set):
            disconnected_ws = {disconnected_ws, }
        self.ws -= disconnected_ws
