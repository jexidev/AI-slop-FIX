class Menu:
    def __init__(self, game_engine): # Add game_engine parameter
        self.game = game_engine # Store game_engine
        self.options = {
            "1": "NEW GAME",
            "2": "LOAD",
            "3": "SETTINGS",
            "4": "QUIT"
        }

    def display_menu(self):
        print("\n--- Main Menu ---")
        for key, value in self.options.items():
            print(f"{key}. {value}")

    def get_choice(self):
        while True:
            choice = input("Enter your choice: ").strip()
            if choice in self.options:
                return self.options[choice]
            else:
                print("Invalid choice. Please try again.")

