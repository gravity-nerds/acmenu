import threading
import time
import json
import os

class AcProto(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)

        self.handle = open(path, "a+")
        self.lineListeners = []
    
    def sendPacket(self, packetid, data):
        self.handle.write(f"<|{packetid}|{json.dumps(data)}\n")

    def run(self):

        self.sendPacket("HI", {})

        while True:
            line = self.handle.readline()
            if line:
                split = line.lstrip().rstrip().split("|")
                
                if len(split) != 3 or len(line) < 3:
                    continue

                (direction, packetid, data) = split

                # Ignore messages from us
                if direction == "<":
                    continue

                data = json.loads(data)

                for listener in self.lineListeners:
                    listener(packetid, data)
            else:
                time.sleep(0.5)
                

    def onLine(self, func):
        self.lineListeners.append(func)

        return func
