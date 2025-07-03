class CommandHandler:
    def __init__(self, game_engine):
        self.game = game_engine

    def handle_command(self):
        if self.game.on_special_tile:
            tile_char = self.game.interaction_manager.current_interaction_tile.character
            prompt_message = ""
            if tile_char == 'X':
                prompt_message = "(y to go to dungeon)"
            elif tile_char == 'N':
                prompt_message = "(y to travel to North Sector)"
            elif tile_char == 'E':
                prompt_message = "(y to travel to East Sector)"
            elif tile_char == 'S':
                prompt_message = "(y to travel to South Sector)"
            elif tile_char == 'W':
                prompt_message = "(y to travel to West Sector)"
            elif tile_char == 'C':
                prompt_message = "(y to return to City Center)"

            key = input(f"Enter a command (w/a/s/d to move, {prompt_message}): ").lower()
            if key == 'y':
                self.game.interaction_manager.travel()
                return False # No movement, but action taken
        else:
            key = input("Enter a command (w/a/s/d to move, q to quit, p to save): ").lower()
        
        # Store player's current position before moving
        prev_x, prev_y = self.game.player.x, self.game.player.y

        moved = False
        if key == 'w':
            self.game.player.move(0, -1, self.game.game_map)
            moved = True
        elif key == 's':
            self.game.player.move(0, 1, self.game.game_map)
            moved = True
        elif key == 'a':
            self.game.player.move(-1, 0, self.game.game_map)
            moved = True
        elif key == 'd':
            self.game.player.move(1, 0, self.game.game_map)
            moved = True
        elif key == 'q':
            self.game.is_running = False
            return False # Indicate no movement, but game is quitting
        elif key == 'p':
            print("--- Save Game ---")
            available_saves = self.game.save_manager.list_saves()
            if available_saves:
                print("Existing saves:")
                for i, save_name in enumerate(available_saves):
                    print(f"  - {save_name}")
            else:
                print("No existing saves.")
            filename = input("Enter save filename (entering an existing name will overwrite it): ")
            self.game.save_manager.save_game(self.game, filename)
            return False # Don't process movement after saving
        elif self.game.on_special_tile and key not in ['w', 'a', 's', 'd']:
            print("Invalid command. Please use w/a/s/d to move or y to advance.")
            return False
        elif not self.game.on_special_tile and key not in ['w', 'a', 's', 'd', 'q', 'p']:
            print("Invalid command. Please use w/a/s/d to move, q to quit, or p to save.")
            return False

        # Check for autosave after a valid move
        if moved and (self.game.player.x != prev_x or self.game.player.y != prev_y): # Only count steps if player actually moved
            self.game.step_count += 1
            if self.game.settings_manager.get_setting("autosave_enabled") and \
               self.game.step_count >= self.game.settings_manager.get_setting("autosave_interval"):
                self.game.save_manager.save_game(self.game, "autosave", is_autosave=True)
                self.game.step_count = 0 # Reset step counter after autosave
            return True # Indicate movement occurred
        return False # No movement occurred