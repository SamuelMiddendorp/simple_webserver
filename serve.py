#!/usr/bin/python
from src.simple_webserver import SimpleWebserver
import os
import sys
def main():
    if(len(sys.argv) > 1):
        # Check if a system argument is provided
        if(sys.argv[1] == "."):
            # When "." is entered we serve the current directory in powershell
            server = SimpleWebserver("0.0.0.0", 8000, os.getcwd())
        else:
            server = SimpleWebserver("0.0.0.0", 8000, sys.argv[1])
    else:
        server = SimpleWebserver("0.0.0.0", 8000)
    server.launch()
if __name__ == '__main__':
    main()