import json
import os
from .utils import clear_screen # Import clear_screen from utils
from .menu import Menu # Import Menu

SETTINGS_FILE = 'settings.json'

class SettingsManager:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading settings: {e}. Using default settings.")
        return self._get_default_settings()

    def _get_default_settings(self):
        return {
            "autosave_enabled": True,
            "autosave_interval": 10 # Steps
        }

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}. Please check file permissions.")

    def get_setting(self, key):
        return self.settings.get(key, self._get_default_settings().get(key))

    def set_setting(self, key, value):
        self.settings[key] = value
        self._save_settings()

class SettingsMenu(Menu): # Inherit from Menu
    def __init__(self, settings_manager, game_engine): # Add game_engine parameter
        super().__init__(game_engine) # Call parent constructor
        self.settings_manager = settings_manager
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.options = {
            "1": "Toggle Autosave",
            "2": "Set Autosave Interval",
            "3": "Back to Main Menu"
        }

    def display_menu(self):
        clear_screen()
        print("\n--- Settings ---")
        print(f"Autosave Enabled: {self.settings_manager.get_setting("autosave_enabled")}")
        print(f"Autosave Interval: {self.settings_manager.get_setting("autosave_interval")} steps")
        for key, value in self.options.items():
            print(f"{key}. {value}")

    def run(self, game_engine): # Accept game_engine as argument
        self.game = game_engine # Set the game engine for the settings menu
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                current_status = self.settings_manager.get_setting("autosave_enabled")
                self.settings_manager.set_setting("autosave_enabled", not current_status)
                print(f"Autosave is now {'Enabled' if not current_status else 'Disabled'}.")
                input("Press Enter to continue...")
            elif choice == "2":
                while True:
                    try:
                        new_interval = int(input("Enter new autosave interval (steps): "))
                        if new_interval > 0:
                            self.settings_manager.set_setting("autosave_interval", new_interval)
                            print(f"Autosave interval set to {new_interval} steps.")
                            break
                        else:
                            print("Interval must be a positive number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                input("Press Enter to continue...")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
