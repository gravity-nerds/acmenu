import json
import os
import logging

from game_manager import GameManager
from menu import Menu 
from libraries.LogFormatter import LogFormatterColorful, LogFormatter

class Core:
    config = None

    # dictionary of threads
    threads = {}

    logger = logging.getLogger()

    def __init__(self):

        if os.path.exists("acmenu.log"):
            os.remove("acmenu.log")

        file_handler = logging.FileHandler("acmenu.log")
        file_handler.setFormatter(LogFormatter())

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(LogFormatterColorful())

        self.logger.setLevel(0)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        # open config.json and read+load the contence
        with open("./config.json") as f:
            self.config = json.loads(f.read())

    def start(self):

        menu = Menu(self)

        self.threads["game_manager"] = GameManager(self)

        self.logger.info("Starting Threads")
        for thread in self.threads.values():
            thread.start()
        
        while self.threads["game_manager"].ready != True:
            pass
        
        self.logger.info("GameManager ready")
        
        
        self.logger.info("Drawing Menu")
        # Run menu on main thread
        menu.run()

def main():
    Core().start()

if __name__ == "__main__":
    main()
