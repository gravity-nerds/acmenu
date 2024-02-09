import threading
import json
import os

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

        with open(f"{path}/acmenu.json") as f:
            game_data = json.loads(f.read())

            assert "friendlyname" in game_data, "acmenu.json: missing {friendlyname:string}"
            assert "version" in game_data, "acmenu.json: missing {version:string}"

        self.games[path.split("/")[-1]] = game_data
            

    def run(self):
        self.load_games(self.acmenu.config["gamesPath"])

        self.ready = True
        
        
        