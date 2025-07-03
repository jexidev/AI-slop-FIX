from src.game_engine import GameEngine
from src.menu import Menu
from src.save_manager import SaveManager
from src.settings_manager import SettingsManager, SettingsMenu
from src.utils import clear_screen
from src.map import Map # Import the Map class

def main():
    # set up the game engine first
    settings_manager = SettingsManager()
    save_manager = SaveManager()
    game_engine = GameEngine(width=20, height=15, settings_manager=settings_manager)  # Pass settings_manager here

    menu = Menu(game_engine)  # then you can pass the game engine through menu

    while True:
        clear_screen()
        menu.display_menu()
        choice = menu.get_choice()

        if choice == "NEW GAME":
            clear_screen()
            # Create the city map first
            city_map = Map(80, 20, map_type="city_center")
            # Pass the city map to the GameEngine
            game = GameEngine(80, 20, settings_manager=settings_manager, game_map=city_map)
            game.run()
        elif choice == "LOAD":
            clear_screen()
            print("--- Load Game ---")
            available_saves = save_manager.list_saves()
            if not available_saves:
                print("No saved games found.")
                input("Press Enter to continue...")
                continue

            print("Available saves:")
            for i, save_name in enumerate(available_saves):
                print(f"{i+1}. {save_name}")
            
            while True:
                try:
                    selection = input("Enter the number of the save to load (or 'b' to go back): ").lower()
                    if selection == 'b':
                        break
                    
                    index = int(selection) - 1
                    if 0 <= index < len(available_saves):
                        loaded_player, loaded_map, map_width, map_height = save_manager.load_game(available_saves[index])
                        if loaded_player and loaded_map:
                            game = GameEngine(map_width, map_height, player=loaded_player, game_map=loaded_map, settings_manager=settings_manager)
                            save_manager.reset_autosave_confirmation() # Reset autosave confirmation for loaded game session
                            game.run()
                        break
                    else:
                        print("Invalid number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number or 'b'.")

        elif choice == "SETTINGS":
            clear_screen()
            settings_menu = SettingsMenu(settings_manager) # Create an instance of SettingsMenu
            settings_menu.run() # Run the settings menu
        elif choice == "QUIT":
            clear_screen()
            print("Exiting game. Goodbye!")
            break

    menu.display()
    
if __name__ == "__main__":  # move this to the bottom so that everything else inside your main() function
    main()
