import os
import threading
import json

from menu import Menu 

class Core:
    config = None

    # dictionary of threads
    threads = {}

    def __init__(self):
        # open config.json and read+load the contence
        with open("./config.json") as f:
            self.config = json.loads(f.read())

    def start(self):
        # start all threads
        for thread in self.threads.values():
            thread.start()
        
        # Create an instance of menu and initialise it
        Menu(self).run()

def main():
    Core().start()

if __name__ == "__main__":
    main()
