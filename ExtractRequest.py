import json
import xmltodict
from Servn.Exceptions import *

def getHeaders(req):
    parts = req.split(" ")
    headersPart = " ".join(parts[2:])
    lines = headersPart.split("\r\n")
    headers = {}
    for line in lines:
        if not line:
            break
        if not line.count(": "):
            continue
        k, v = line.split(": ")[:2]
        headers[k] = v
    return headers

def getBody(req, forceContentType=None):
    body = ""
    contentType = "brut"
    if req.count("\r\n\r\n"):
        body = req.split("\r\n\r\n")[-1]
        try:
            body = xmltodict.parse(body)
            contentType = "xml"
        except:
            try:
                body = json.loads(body)
                contentType = "json"
            except:
                pass
    if forceContentType is not None and contentType != forceContentType:
        raise BodyContentTypeError(f"Body Type: {contentType}. Expected: {forceContentType}")
    return body
