import random
from .tiles import FloorTile, WallTile, NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile # Import new Tile classes

class Map:
    def __init__(self, width, height, map_type="dungeon", generate=True, entry_direction=None):
        self.width = width
        self.height = height
        self.grid = [[WallTile() for _ in range(width)] for _ in range(height)]
        self.room_centers = []
        self.next_map_tile_pos = None
        self.current_map_type = map_type # Store the current map type

        if generate:
            if map_type == "dungeon":
                self.generate_dungeon()
            elif map_type == "city_center":
                self.generate_city_center()
            elif map_type == "outer_city":
                self.generate_outer_city(entry_direction)

    def generate_city_center(self):
        # Fill the entire map with floor tiles
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = FloorTile()

        # Place the 'X' tile to enter the dungeon (still exists in city center)
        dungeon_entrance_x = self.width // 2
        dungeon_entrance_y = self.height // 2
        self.grid[dungeon_entrance_y][dungeon_entrance_x] = NextMapTile()
        self.next_map_tile_pos = (dungeon_entrance_x, dungeon_entrance_y)

        # Place North exit (N)
        self.grid[2][self.width // 2] = NorthExitTile()
        # Place East exit (E)
        self.grid[self.height // 2][self.width - 3] = EastExitTile()
        # Place South exit (S)
        self.grid[self.height - 3][self.width // 2] = SouthExitTile()
        # Place West exit (W)
        self.grid[self.height // 2][2] = WestExitTile()

        # --- Blacksmith Shop ---
        # Top-left corner of the shop
        shop_start_x = 1
        shop_start_y = 1
        shop_width = 7
        shop_height = 5

        # Place top and bottom walls
        for x in range(shop_start_x, shop_start_x + shop_width):
            self.grid[shop_start_y][x] = WallTile() # Top wall
            self.grid[shop_start_y + shop_height - 1][x] = WallTile() # Bottom wall

        # Place side walls
        for y in range(shop_start_y, shop_start_y + shop_height):
            self.grid[y][shop_start_x] = WallTile() # Left wall
            self.grid[y][shop_start_x + shop_width - 1] = WallTile() # Right wall

        # Place the Blacksmith Shop entrance tile
        self.grid[shop_start_y + 2][shop_start_x + shop_width - 1] = BlacksmithShopTile() # 'B' tile

        # Place the doorway (East exit from the shop)
        self.grid[shop_start_y + 2][shop_start_x + shop_width] = EastExitTile() # 'E' tile

        # Set a default spawn point for the player in the city center
        self.room_centers.append((self.width // 2, self.height // 2 + 5))

    def generate_outer_city(self, entry_direction):
        # Fill the entire map with floor tiles
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = FloorTile()

        # Place the City Center Entrance tile ('C') based on entry_direction
        if entry_direction == "north":
            self.grid[self.height - 3][self.width // 2] = CityCenterEntranceTile()
            self.room_centers.append((self.width // 2, self.height - 4)) # Spawn just above 'C'
        elif entry_direction == "east":
            self.grid[self.height // 2][2] = CityCenterEntranceTile()
            self.room_centers.append((3, self.height // 2)) # Spawn just right of 'C'
        elif entry_direction == "south":
            self.grid[2][self.width // 2] = CityCenterEntranceTile()
            self.room_centers.append((self.width // 2, 3)) # Spawn just below 'C'
        elif entry_direction == "west":
            self.grid[self.height // 2][self.width - 3] = CityCenterEntranceTile()
            self.room_centers.append((self.width - 4, self.height // 2)) # Spawn just left of 'C'
        else: # Default or error case, place in center
            self.grid[self.height // 2][self.width // 2] = CityCenterEntranceTile()
            self.room_centers.append((self.width // 2, self.height // 2))

    def generate_dungeon(self):
        rooms = []
        for _ in range(10):
            room_width = random.randint(5, 12)
            room_height = random.randint(5, 12)
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)

            for y in range(room_y, room_y + room_height):
                for x in range(room_x, room_x + room_width):
                    self.grid[y][x] = FloorTile()
            
            center_x = room_x + room_width // 2
            center_y = room_y + room_height // 2
            rooms.append((center_x, center_y))
            self.room_centers.append((center_x, center_y))

        for i in range(len(rooms) - 1):
            self.create_corridor(rooms[i], rooms[i+1])

        # Place the next map tile ('?') far from the player's initial spawn
        player_spawn_x, player_spawn_y = self.get_random_room_center()
        
        # --- DEBUG FEATURE: Force X tile near player ---
        DEBUG_FORCE_X_TILE_NEAR_PLAYER = False # Set to False to disable

        if DEBUG_FORCE_X_TILE_NEAR_PLAYER:
            # Try to place one step to the right
            target_x = player_spawn_x + 1
            target_y = player_spawn_y
            if 0 < target_x < self.width - 1:
                self.grid[target_y][target_x] = FloorTile() # Ensure it's a floor tile
                self.next_map_tile_pos = (target_x, target_y)
            else:
                # If right is not possible, try one step to the left
                target_x = player_spawn_x - 1
                if 0 < target_x < self.width - 1:
                    self.grid[target_y][target_x] = FloorTile() # Ensure it's a floor tile
                    self.next_map_tile_pos = (target_x, target_y)
                else:
                    # Fallback to random if neither immediate horizontal spot is suitable
                    self._place_random_x_tile(player_spawn_x, player_spawn_y)
        else:
            # Original logic for random placement
            self._place_random_x_tile(player_spawn_x, player_spawn_y)

    def _place_random_x_tile(self, player_spawn_x, player_spawn_y):
        max_attempts = 1000
        for _ in range(max_attempts):
            tile_x = random.randint(1, self.width - 2)
            tile_y = random.randint(1, self.height - 2)

            if self.grid[tile_y][tile_x].is_walkable and \
               self._distance((tile_x, tile_y), (player_spawn_x, player_spawn_y)) > (self.width + self.height) / 3:
                self.next_map_tile_pos = (tile_x, tile_y)
                self.grid[tile_y][tile_x] = NextMapTile()
                return # Success

        # Fallback: If a distant spot isn't found, place it on the first available floor tile.
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x].is_walkable:
                    self.next_map_tile_pos = (x, y)
                    self.grid[y][x] = NextMapTile()
                    return

    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return not self.grid[y][x].is_walkable # Check is_walkable property
        return True # Treat out-of-bounds as walls

    def get_tile_type(self, x, y):
        """Returns the character at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].character # Return character property
        return '#' # Treat out-of-bounds as walls

    

    def _distance(self, p1, p2):
        """Calculates the Euclidean distance between two points."""
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    def create_corridor(self, start, end):
        x1, y1 = start
        x2, y2 = end

        # Randomly choose to go horizontal then vertical, or vice versa
        if random.random() < 0.5:
            # Horizontal first
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[y1][x] = FloorTile()
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[y][x2] = FloorTile()
        else:
            # Vertical first
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[y][x1] = FloorTile()
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[y2][x] = FloorTile()

    def get_random_room_center(self):
        if not self.room_centers:
            # Fallback for dungeons, or default for city
            return self.width // 2, self.height // 2
        return random.choice(self.room_centers)

    def to_dict(self):
        # Convert grid of Tile objects to their dictionary representations
        grid_data = [[tile.to_dict() for tile in row] for row in self.grid]
        return {
            "width": self.width,
            "height": self.height,
            "grid": grid_data,
            "room_centers": self.room_centers,
            "next_map_tile_pos": self.next_map_tile_pos
        }

    @classmethod
    def from_dict(cls, data):
        game_map = cls(data["width"], data["height"], generate=False) # Pass generate=False
        # Reconstruct Tile objects from their dictionary representations
        from .tiles import FloorTile, WallTile, NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile # Import inside to avoid circular dependency
        tile_type_map = {
            "FloorTile": FloorTile,
            "WallTile": WallTile,
            "NextMapTile": NextMapTile,
            "NorthExitTile": NorthExitTile,
            "EastExitTile": EastExitTile,
            "SouthExitTile": SouthExitTile,
            "WestExitTile": WestExitTile,
            "CityCenterEntranceTile": CityCenterEntranceTile,
            "BlacksmithShopTile": BlacksmithShopTile
        }
        game_map.grid = []
        for row_data in data["grid"]:
            row = []
            for tile_data in row_data:
                tile_type = tile_type_map.get(tile_data["type"])
                if tile_type:
                    row.append(tile_type()) # Recreate instance based on type
                else:
                    # Fallback for unknown tile types, or raise an error
                    row.append(FloorTile()) # Default to floor
            game_map.grid.append(row)

        game_map.room_centers = data["room_centers"]
        game_map.next_map_tile_pos = tuple(data["next_map_tile_pos"]) if data["next_map_tile_pos"] else None
        return game_map
