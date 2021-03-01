# simple_webserver

##### A simple abstraction for a webserver using sockets

### Why?

For fun of course! I've always wanted to get into networking and this is a good place to start,

### How?

Getting started is simple. Simply import SimpleWebserver, provide a host and port and voilá.

(currently the server is always serving a set html response)

```python
from simple_webserver import SimpleWebServer
def main():
    server = SimpleWebServer('0.0.0.0', 8000)
    server.launch()
if __name__ == '__main__':
    main()
```



Use `ctrl-c`  to shutdown at any moment during execution