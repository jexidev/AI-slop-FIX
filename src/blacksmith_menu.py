from .menu import Menu

class BlacksmithMenu(Menu):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.options = [
            "Buy",
            "Sell",
            "Upgrade",
            "Exit"
        ]

    def display(self):
        self.game.clear_screen()
        print("\n--- Blacksmith Shop ---")
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option}")
        print("-----------------------")

    def handle_input(self, choice):
        if choice == "1":
            self.game.display_message("You browse the wares.")
            # Implement buy logic
        elif choice == "2":
            self.game.display_message("You offer items for sale.")
            # Implement sell logic
        elif choice == "3":
            self.game.display_message("You consider upgrading your gear.")
            # Implement upgrade logic
        elif choice == "4":
            self.game.display_message("You leave the blacksmith shop.")
            self.game.current_menu = None # Exit the blacksmith menu
        else:
            self.game.display_message("Invalid choice.")