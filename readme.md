# Servn

This module let you create your web-service in the simplest way possible.

## Installation
```bash
pip install servn
```

## 📂 File Structure Overview

| File               | Description                                   |
|--------------------|-----------------------------------------------|
| `Framework.py`     | Core routing and request handling system      |
| `Server.py`        | HTTP server implementation with threading     |
| `Response.py`      | HTTP response builder with JSON/file support  |
| `Constants.py`     | MIME type mappings for file extensions        |
| `Exceptions.py`    | Custom exceptions for the framework           |
| `ExtractRequest.py`| HTTP request parser (headers/body)            |
| `Freemarker.py`    | Template engine with conditional logic        |
| `Supplier.py`      | Class duplication utility                     |
| `typesCheck.py`    | Runtime type validation system                |
| `utils.py`        | File system utilities and helpers             |


## ❗ For a code example, check example.md
# Files documentations

## 🧩 Framework.py

The ```Framework.py``` module implements the core logic of the Servn web framework. It manages routing, request handling, and dispatching incoming HTTP requests to the appropriate handler functions based on their HTTP method (GET, POST, etc.) and path.

This module allows you to easily define routes using decorators such as ```@framework.get(path)``` or ```@framework.post(path)```. Each route is associated with a Python function that processes the request and returns a response.

Key features of Framework.py include:

- Route registration: Supports dynamic path matching and route binding for HTTP methods.

- Request dispatching: Automatically invokes the correct route handler when a request arrives.

- Middleware and extensibility: Designed for easy expansion with additional features or middleware layers.

This is the heart of Servn's minimalistic and flexible approach to building web services, enabling quick development with simple syntax and clear separation of concerns.

```Python
# Example usage of route decorator
@fw.get(path="/hello")
def hello_world(request):  # request -> request.method, request.path, request.headers, request.body
    return Response.create(status="200 OK", body="Hello, world!").build()
```

If the path is None, this method acts as a catch-all handler, invoked for every GET request that does not match a more specific registered route.
```Python
@fw.get(path="/hello")
def hello_world(request):  # request -> request.method, request.path, request.headers, request.body
    return Response.create(status="200 OK", body="Hello, world!").build()

@fw.get()
def catchAll():  # Called if the path isn't "/hello"
    return Response.create(status="200 OK", body="A GET request").build()
```

__For more details, check FrameworkDoc.md__

## 🧩 Server.py

The ```Server.py``` module provides the underlying HTTP server implementation for the Servn framework. It handles low-level networking tasks such as binding to an IP address and port, accepting incoming socket connections, and managing concurrent client requests using threading.

Key features:
- Socket management: Creates a TCP socket server that listens on a specified IP and port.

- Threaded connections: For each incoming connection, a new thread is spawned to handle the client request independently, enabling multiple simultaneous connections.

- Framework integration: Upon accepting a connection, it creates a fresh instance of the Servn framework handler (by duplicating the framework object) and delegates processing of the request to this instance.

- Simple server loop: Continuously accepts new connections until stopped.

This module acts as the bridge between raw network requests and the higher-level routing and request handling provided by the framework.

```Python
# Example of starting the server
fw = Framework()
server = Server.Bind("127.0.0.1", 5555, fw)
server.run()
```
When a client connects, the server spawns a new thread, duplicates the framework instance, and calls the ```process``` method on the new instance to handle the request lifecycle. This design ensures isolation and thread-safety for concurrent requests.

## 🧩 Freemarker.py

The ```Freemarker.py``` module implements a lightweight template engine for Servn, inspired by the popular FreeMarker template system. It allows you to create dynamic text output by embedding placeholders and conditional logic within template strings.

Key features:
Placeholder substitution: Replace placeholders in the template (e.g., ```${variable}```) with corresponding values from a provided context dictionary.

- Conditional blocks: Supports simple if constructs within templates to conditionally include or exclude parts of the output based on boolean expressions.

- Simple syntax: Enables fast templating without the complexity of full-fledged engines, ideal for small to medium web responses.

- Seamless integration: Works smoothly with Servn’s ```Exchange``` properties or any key-value data structure.

This module is perfect for generating HTML, plain text, or any formatted content dynamically, providing flexibility in response rendering.
Here's an example of use:

```Python
class Alice:
    name = "Alice"
    friends = {"Doria": "my best friend", "Marco": "a good friend"}

template = """My name is ${person.name} and Marco is ${person.friends.Marco}"""

ctx = {"person": Alice}
templateEngine = Freemarker.TemplateEngine(template, ctx)
print(templateEngine.process())
```
Output: 
```Text
My name is Alice and Marco is a good friend
```

