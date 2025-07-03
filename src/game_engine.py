from .map import Map
from .player import Player
from .save_manager import SaveManager
from .settings_manager import SettingsManager # Import SettingsManager
import os
from .utils import clear_screen
from .command_handler import CommandHandler # Import CommandHandler
from .interaction_manager import InteractionManager # Import InteractionManager
from .blacksmith_menu import BlacksmithMenu # Import BlacksmithMenu

class GameEngine:
    def __init__(self, width, height, player=None, game_map=None, settings_manager=None):
        self.is_running = True
        self.game_map = game_map if game_map else Map(width, height)
        self.player = player if player else Player(*self.game_map.get_random_room_center())
        self.save_manager = SaveManager()
        self.save_manager.reset_autosave_confirmation() # Reset autosave confirmation for new game session
        self.settings_manager = settings_manager # Store SettingsManager instance
        self.step_count = 0 # Initialize step counter for autosave
        self.temp_message = None # Initialize temporary message
        self.command_handler = CommandHandler(self) # Initialize CommandHandler
        self.interaction_manager = InteractionManager(self) # Initialize InteractionManager
        self.on_special_tile = False # New flag for special tile interaction
        self.current_menu = None # To manage active menus (e.g., blacksmith, inventory)
        self.blacksmith_menu = BlacksmithMenu(self) # Initialize BlacksmithMenu

    def set_temp_message(self, message):
        self.temp_message = message

    def run(self):
        while self.is_running:
            self.render()
            if self.current_menu:
                self.current_menu.display()
            self.process_input()
            self.update()
            self.interaction_manager.handle_interactions()

    def process_input(self):
        if self.current_menu:
            choice = input("Enter choice: ").strip()
            self.current_menu.handle_input(choice)
        else:
            self.command_handler.handle_command()

    def display_blacksmith_menu(self):
        self.current_menu = self.blacksmith_menu

        

    def update(self):
        # Game logic updates go here
        pass

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.game_map.height):
            row_str = ""
            for x in range(self.game_map.width):
                tile_char = self.game_map.get_tile_type(x, y)
                if x == self.player.x and y == self.player.y:
                    row_str += '@'
                else:
                    row_str += tile_char
            print(row_str)
        
        print(f"Health: {self.player.health}/{self.player.max_health} Attack: {self.player.attack} Defense: {self.player.defense})")

        # Display Blacksmith Shop name if player is inside
        shop_start_x = 1
        shop_start_y = 1
        shop_width = 7
        shop_height = 5

        if shop_start_x <= self.player.x < shop_start_x + shop_width and \
           shop_start_y <= self.player.y < shop_start_y + shop_height:
            print("Blacksmith Shop")

        if self.temp_message:
            print(self.temp_message)
            self.temp_message = None # Clear the message after displaying