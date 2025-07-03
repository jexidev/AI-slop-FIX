import json
import os
from .map import Map
from .player import Player

SAVE_DIR = "saves"

class SaveManager:
    def __init__(self):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        self._autosave_overwrite_confirmed = None # None: not asked, True: confirmed, False: denied

    def _get_save_path(self, filename):
        return os.path.join(SAVE_DIR, filename + ".json")

    def save_game(self, game_engine, filename, is_autosave=False):
        game_state = {
            "player": game_engine.player.to_dict(),
            "map": game_engine.game_map.to_dict(),
            "map_width": game_engine.game_map.width,
            "map_height": game_engine.game_map.height
        }
        
        save_path = self._get_save_path(filename)

        if is_autosave and filename == "autosave":
            if self._autosave_overwrite_confirmed is False:
                # User previously denied autosave overwrite for this session
                print("Autosave skipped for this session.")
                return
            elif self._autosave_overwrite_confirmed is None and os.path.exists(save_path):
                # Ask for confirmation only once per session if file exists
                confirm = input(f"Autosave file '{filename}' already exists. Overwrite for this session? (y/n): ").lower()
                if confirm == 'y':
                    self._autosave_overwrite_confirmed = True
                    game_engine.set_temp_message("Game Autosaved!")
                else:
                    self._autosave_overwrite_confirmed = False
                    print("Autosave skipped for this session.")
                    return
            elif self._autosave_overwrite_confirmed is True:
                # User previously confirmed, proceed silently
                game_engine.set_temp_message("Game Autosaved!")
        else:
            # Manual save or non-autosave filename, always ask for overwrite if file exists
            if os.path.exists(save_path):
                confirm = input(f"Save file '{filename}' already exists. Overwrite? (y/n): ").lower()
                if confirm != 'y':
                    print("Save cancelled.")
                    return

        with open(save_path, 'w') as f:
            json.dump(game_state, f, indent=4)
        print(f"Game saved to {save_path}")

    def reset_autosave_confirmation(self):
        self._autosave_overwrite_confirmed = None

    def load_game(self, filename):
        save_path = self._get_save_path(filename)
        if not os.path.exists(save_path):
            print(f"Error: Save file {filename}.json not found.")
            return None

        with open(save_path, 'r') as f:
            game_state = json.load(f)

        # Reconstruct game objects
        loaded_player = Player.from_dict(game_state["player"])
        loaded_map = Map.from_dict(game_state["map"])
        
        print(f"Game loaded from {save_path}")
        return loaded_player, loaded_map, game_state["map_width"], game_state["map_height"]

    def list_saves(self):
        saves = []
        if os.path.exists(SAVE_DIR):
            for filename in os.listdir(SAVE_DIR):
                if filename.endswith(".json"):
                    saves.append(filename[:-5]) # Remove .json extension
        return saves
