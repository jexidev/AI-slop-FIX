from .entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack=10, defense=5) # Initial player stats

    def move(self, dx, dy, game_map):
        if dx != 0 and dy == 0: # Horizontal movement
            # Define potential steps
            step1_x, step1_y = self.x + dx, self.y + dy
            step2_x, step2_y = self.x + (dx * 2), self.y + (dy * 2)
            step3_x, step3_y = self.x + (dx * 3), self.y + (dy * 3)

            # Check for next map tile at step 1
            if game_map.next_map_tile_pos and step1_x == game_map.next_map_tile_pos[0] and step1_y == game_map.next_map_tile_pos[1]:
                if not game_map.is_wall(step1_x, step1_y):
                    self.x, self.y = step1_x, step1_y
                return

            # Attempt three-step move
            if not game_map.is_wall(step1_x, step1_y) and \
               not game_map.is_wall(step2_x, step2_y) and \
               not game_map.is_wall(step3_x, step3_y):
                self.x, self.y = step3_x, step3_y
            # Attempt two-step move
            elif not game_map.is_wall(step1_x, step1_y) and \
                 not game_map.is_wall(step2_x, step2_y):
                self.x, self.y = step2_x, step2_y
            # Attempt one-step move
            elif not game_map.is_wall(step1_x, step1_y):
                self.x, self.y = step1_x, step1_y
        else: # Vertical movement
            new_x = self.x + dx
            new_y = self.y + dy
            if not game_map.is_wall(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        # When loading, we need to reconstruct the Player using the Entity's from_dict
        # and then ensure it's an instance of Player.
        player = Entity.from_dict(data)
        # Create a Player instance and copy attributes from the loaded Entity
        new_player = cls(player.x, player.y) # Initialize with x, y
        new_player.max_health = player.max_health
        new_player.health = player.health
        new_player.attack = player.attack
        new_player.defense = player.defense
        return new_player
