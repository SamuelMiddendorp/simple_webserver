#!/usr/bin/python
from src.simple_webserver import SimpleWebserver
def main():
    server = SimpleWebserver("0.0.0.0", 8000)
    server.launch()
if __name__ == '__main__':
    main()