import subprocess
import threading
import json
import os

def DecodePacket(line):
    split = line.lstrip().rstrip().split("|")
                
    if len(split) != 3 or len(line) < 3:
        raise ValueError("line is not properly formmated", line)

    (direction, packetid, data) = split

    data = json.loads(data)

    return direction, packetid, data

def EncodePacket(direction, packetid, data):
    return f"{direction}|{packetid}|{json.dumps(data)}"

class Connection(threading.Thread):
    def __init__(self, path, process):
        threading.Thread.__init__(self)

        self.path = path
        self.process = process
        print(path+"/acproto")
        if os.path.exists(path + "/acproto"):
            os.remove(path + "/acproto")
        self.stream = open(path + "/acproto", "a+")

    def sendPacket(self, packetid, data):
        print("sending packet", packetid, data)
        self.stream.write(EncodePacket(">", packetid, data))

    def run(self):
        while True:
            line = self.stream.readline()
            if len(line) >= 3:
                direction, packetid, _ = DecodePacket(line)

                if direction == "<" and packetid == "HI":
                    break

        while True:
            line = self.stream.readline()
            if len(line) >= 3:
                direction, packetid, data = DecodePacket(line)

                if direction == ">":
                    continue

                match packetid:
                    case "HI":
                        self.sendPacket("STATUS", {"message": "existing"})





class GameManager(threading.Thread):

    current = None
    ready = False
    games = {}

    def __init__(self, acmenu):
        threading.Thread.__init__(self)

        self.acmenu = acmenu

    def load_games(self, path):
        for folder_name in os.listdir(path):
            try:
                self.load_game(path + f"/{folder_name}")
            except Exception as e:
                self.acmenu.logger.error(f"Failed to load {folder_name} | {e}")
        
        self.acmenu.logger.info(f"Loaded {len(self.games)} game(s)")

    def load_game(self, path):
        assert os.path.exists(f"{path}/acmenu.json"), "missing acmenu.json"
        assert os.path.exists(f"{path}/run.sh"), "missing run.json"

        id = path.split("/")[-1]

        with open(f"{path}/acmenu.json") as f:
            game_data = json.loads(f.read())

            assert "friendlyname" in game_data, "acmenu.json: missing {friendlyname:string}"
            assert "version" in game_data, "acmenu.json: missing {version:string}" 

            game_data["id"] = id
            game_data["path"] = path 

        self.games[id] = game_data

    def start_game(self, id):
        game = self.games[id]

        current = subprocess.Popen([
            "bash",
            "./run.sh",
        ], cwd=game["path"])

        connection = Connection(game["path"], current)
        connection.start()

    def run(self):
        self.load_games(self.acmenu.config["gamesPath"])

        self.ready = True
        