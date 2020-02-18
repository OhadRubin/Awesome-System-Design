import socket


class Connection:
    @classmethod
    def connect(cls, host, port):
        conn = socket.socket()
        conn.connect(tuple([host, port]))
        return cls(conn)

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        normalize = lambda x: x[0] + ":" + str(x[1])
        me = normalize(self.socket.getsockname())
        peer = normalize(self.socket.getpeername())
        return f"<Connection from {me} to {peer}>"

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        packet = b''
        while True:
            buffer = self.socket.recv(size)
            if not buffer:
                raise Exception
            packet += buffer
            if len(packet) == size:
                break
        return packet

    def receive_all(self):
        packet = b''
        while True:
            buffer = self.socket.recv(512)
            if not buffer:
                return packet
            packet += buffer

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
