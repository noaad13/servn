import typesCheck

class New:
    method: str
    path: str
    headers: dict
    body: object

    @typesCheck.require(method=str, path=str, headers=dict)
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    def __repr__(self):
        return f"method: {self.method}\npath: {self.path}\nheaders: {self.headers}\nbody: {self.body}"
