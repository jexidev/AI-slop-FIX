from .map import Map
from .tiles import NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile

class InteractionManager:
    def __init__(self, game_engine):
        self.game = game_engine
        self.current_interaction_tile = None # Store the tile being interacted with

    def handle_interactions(self):
        player_x, player_y = self.game.player.x, self.game.player.y
        current_tile = self.game.game_map.grid[player_y][player_x]

        if isinstance(current_tile, (NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile)):
            self.game.on_special_tile = True
            self.current_interaction_tile = current_tile
        else:
            self.game.on_special_tile = False
            self.current_interaction_tile = None

    def travel(self):
        if isinstance(self.current_interaction_tile, NextMapTile):
            print("Generating new dungeon map...")
            self.game.game_map = Map(self.game.game_map.width, self.game.game_map.height, map_type="dungeon")
            player_start_x, player_start_y = self.game.game_map.get_random_room_center()
            self.game.player.x = player_start_x
            self.game.player.y = player_start_y
        elif isinstance(self.current_interaction_tile, NorthExitTile):
            print("Traveling to North Sector...")
            self.game.game_map = Map(self.game.game_map.width, self.game.game_map.height, map_type="outer_city", entry_direction="north")
            player_start_x, player_start_y = self.game.game_map.get_random_room_center()
            self.game.player.x = player_start_x
            self.game.player.y = player_start_y
        elif isinstance(self.current_interaction_tile, EastExitTile):
            print("Traveling to East Sector...")
            self.game.game_map = Map(self.game.game_map.width, self.game.game_map.height, map_type="outer_city", entry_direction="east")
            player_start_x, player_start_y = self.game.game_map.get_random_room_center()
            self.game.player.x = player_start_x
            self.game.player.y = player_start_y
        elif isinstance(self.current_interaction_tile, SouthExitTile):
            print("Traveling to South Sector...")
            self.game.game_map = Map(self.game.game_map.width, self.game.game_map.height, map_type="outer_city", entry_direction="south")
            player_start_x, player_start_y = self.game.game_map.get_random_room_center()
            self.game.player.x = player_start_x
            self.game.player.y = player_start_y
        elif isinstance(self.current_interaction_tile, WestExitTile):
            print("Traveling to West Sector...")
            self.game.game_map = Map(self.game.game_map.width, self.game.game_map.height, map_type="outer_city", entry_direction="west")
            player_start_x, player_start_y = self.game.game_map.get_random_room_center()
            self.game.player.x = player_start_x
            self.game.player.y = player_start_y
        elif isinstance(self.current_interaction_tile, CityCenterEntranceTile):
            print("Returning to City Center...")
            self.game.game_map = Map(self.game.game_map.width, self.game.game_map.height, map_type="city_center")
            player_start_x, player_start_y = self.game.game_map.get_random_room_center()
            self.game.player.x = player_start_x
            self.game.player.y = player_start_y
        elif isinstance(self.current_interaction_tile, BlacksmithShopTile):
            self.game.display_blacksmith_menu()