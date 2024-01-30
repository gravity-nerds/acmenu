import os
import threading
import json

import menu

class main:

    config = None
    threads = {}

    def __init__(self):
        with open("./acmenu/config.json") as f:
            self.config = json.loads(f.read())

    def start(self):
        self.threads["menu"] = 
        

main()