import sys, asyncio

def check_python_version():
    version = sys.version_info

    if (version < (3, 10)):
        print("[-] GitSint only works with Python 3.10+.")
        exit("-> Go install the most recent version of python -> https://www.python.org/downloads/")

    else:
        from lib.cli import parser; asyncio.run(parser())