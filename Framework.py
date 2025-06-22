import socket
from Servn import Response as _Response
from Servn import ExtractRequest as _ER
from .models import Request
import json

ELSE = 0x00

class Framework:
    routes = {}

    def __init__(self):
        self.routes = {}
        self.get_routes = {}
        self.post_routes = {}

    def route(self, path=None):
        if path is None:
            path = ELSE

        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def get(self, path=None):
        if path is None:
            path = ELSE

        def decorator(func):
            self.get_routes[path] = func
            return func
        return decorator

    def post(self, path=None, forceContent=None):
        if path is None:
            path = ELSE

        def decorator(func):
            self.post_routes[path] = [func, forceContent]
            return func
        return decorator

    def process(self, conn: socket.socket):
        conn.settimeout(1)
        try:
            req = conn.recv(4096).decode("utf-8", errors="ignore")
        except:
            return
        parts = req.split()
        if len(parts) < 2:
            return
        parts = parts[:2]
        method, path = parts
        headers = _ER.getHeaders(req)
        headers["path"] = path
        force = None
        if method == "POST":
            if path in self.post_routes:
                force = self.post_routes[path][1]
            elif ELSE in self.post_routes:
                force = self.post_routes[ELSE][1]
        try:
            body = _ER.getBody(req, forceContentType=force)
        except:
            body = None
        request = Request.New(method, path, headers, body)
        if method == "GET":
            if path in self.get_routes:
                resp = self.get_routes[path](request)
                conn.sendall(resp)
                conn.close()
                return
            elif ELSE in self.get_routes:
                resp = self.get_routes[ELSE](request)
                conn.sendall(resp)
                conn.close()
                return
        elif method == "POST":
            if body is None:
                conn.sendall(_Response.create(status="400 Bad Request", body="Invalid datas").build())
                conn.close()
                return
            if path in self.post_routes:
                resp = self.post_routes[path][0](request)
                conn.sendall(resp)
                conn.close()
                return
            elif ELSE in self.post_routes:
                resp = self.post_routes[ELSE][0](request)
                conn.sendall(resp)
                conn.close()
                return
        if ELSE in self.routes:
            resp = self.routes[ELSE](request)
            conn.sendall(resp)
        else:
            resp = _Response.create(status="404 Not Found", body="404 Not found", contentType=_Response.BRUT).build()
            conn.sendall(resp)
        conn.close()
