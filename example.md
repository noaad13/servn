# Advanced Code Example

```Python
from Servn import Framework, Server, Response, Freemarker

fw = Framework.Framework()
serv = Server.Bind("127.0.0.1", 3333, fw)

@fw.get()

```
