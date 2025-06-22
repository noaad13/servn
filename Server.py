import socket
import threading
from Servn import Supplier, typesCheck

class Bind:
    ip: str
    port: int

    @typesCheck.require(host=str, port=int)
    def __init__(self, ip, port, framework):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((ip, port))
        self.sock.listen()
        self.fw = framework

    def fw_instancy(self, conn):  # Copy the framework in a new class and launch the process method
        new = Supplier.duplicate(self.fw.__class__, {}, {"routes": self.fw.routes, "get_routes": self.fw.get_routes,
                                                         "post_routes": self.fw.post_routes})
        new.process(conn)

    def run(self, disableWarning=False):
        if not disableWarning:
            print(f"Server running on {self.ip}:{self.port}\n")
        while True:
            conn, _ = self.sock.accept()
            threading.Thread(target=self.fw_instancy, args=(conn, )).start()
