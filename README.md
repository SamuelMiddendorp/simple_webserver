# simple_webserver

##### A simple abstraction for a webserver using sockets

### Why?

For fun of course! I've always wanted to get into networking and this is a good place to start,

### How?

####  In your own implementation

Getting started is simple. Simply import SimpleWebserver, provide a host and port et voilá.

```python
from src.simple_webserver import SimpleWebserver
def main():
    server = SimpleWebserver("0.0.0.0", 8000)
    server.launch()
if __name__ == "__main__":
    main()
```

Alternatively you could specify a file path for the server to serve.

```python
server = SimpleWebserver("0.0.0.0", 8000, "C:/documents/mysimplewebapp")
```

Run your server implementation in any terminal ``PS: D\documents> python myimplementation.py`` 

Use `ctrl-c`  to shutdown at any moment. 

### Standalone

For the standalone version it is highly advised to copy `SimpleWebserver.py` into a folder thats linked to your path variable in windows. Like your python installation folder. This will make sure you can call it from any directory in shell.

Running ``SimpleWebserver.py`` will start a server based on the argument you pass to it in the command line:

Passing in no arguments will serve the files in the directory `SimpleWebserver.py` is in.

Passing `.` will serve the files in the current directory in your shell.

Passing in a absolute file path will serve the files located at that path.

Use `ctrl-c`  to shutdown at any moment. 



