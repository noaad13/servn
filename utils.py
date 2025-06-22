import os

DIRECTORY = os.getcwd() + "\\"

def fRead(path, bytesContent=False):
    mode = "r"
    if bytesContent:
        mode = "rb"
    with open(path, mode) as f:
        content = f.read()
        f.close()
    return content

def fWrite(path, content):
    if isinstance(content, str):
        mode = ""
    elif isinstance(content, bytes):
        mode = "b"
    else:
        raise TypeError("content argument must be str or bytes")
    with open(path, "w" + mode) as f:
        f.write(content)
        f.flush()
        f.close()

def fAdd(path, content):
    before = fRead(path, bytesContent=isinstance(content, bytes))
    fWrite(path, before + content)

def abspath(path):
    path = path.replace("/", "\\")
    if path[1:3] == ":\\":
        return path
    return DIRECTORY + path

def existsFile(path):
    try:
        open(path, "r").close()
        return True
    except:
        return False
