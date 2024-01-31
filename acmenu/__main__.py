import os
import threading
import json

from menu import Menu 

class Core:

    config = None
    threads = {}

    def __init__(self):
        with open("./acmenu/config.json") as f:
            self.config = json.loads(f.read())

    def start(self):
        self.threads["menu"] = Menu(self)

        for thread in self.threads.values():
            thread.start()
        

def main():
    core = Core()
    core.start()


if __name__ == "__main__":
    main()