import json
import os

from Servn import Constants, utils, typesCheck

DETECT = "detect"
BRUT = "text/plain"
JSON = "application/json"

class create:
    @typesCheck.require(status=str, body=object, contentType=str)
    def __init__(self, status, body, contentType=BRUT):
        self.status = status
        self.body = body
        self.contentType = contentType

    @typesCheck.require(status=str, body=object, contentType=str)
    def config(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError("You tried to config an unknown parameter")
        return self

    def build(self):
        body = self.body
        if self.contentType == Constants.CONTENT_TYPES[".json"]:
            if isinstance(body, dict):
                body = json.dumps(body)
        response = (
            f"HTTP/1.1 {self.status}\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            f"Content-Type: {self.contentType}\r\n"
            f"\r\n"
            f"{body}"
        ).encode()
        return response

class File:
    path: str
    status: str
    contentType: str

    @typesCheck.require(path=str, status=str)
    def __init__(self, path, status, contentType=""):
        self.path = path
        self.status = status
        self.contentType = contentType

    @typesCheck.require(path=str, status=str)
    def config(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError("You tried to config an unknown parameter")
        return self

    def build(self):
        contentType = self.contentType
        if not contentType or contentType == DETECT:
            ext = "." + self.path.split(".")[-1]
            contentType = Constants.CONTENT_TYPES.get(ext)
            if not contentType:
                contentType = Constants.CONTENT_TYPES[".txt"]
        if os.path.exists(self.path):
            body = utils.fRead(self.path, bytesContent=True)
            status = self.status.encode()
        else:
            status = b"404"
            body = b"404 Not Found"
        response = (
                b"HTTP/1.1" + status + b"\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"Content-Type: " + contentType.encode() + b"\r\n\r\n" + body
        )
        return response
