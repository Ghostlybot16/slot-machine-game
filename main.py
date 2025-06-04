from services.logic import SlotMachine
from services.ui import deposit, get_bet, get_number_of_slot_lines, print_slot_machine

class Game:
    """
    A class to manage the slot machine game flow and user balance.
    """

    # Constants for game configuration
    MAX_LINES = 3   # Maximum number of lines a play can bet on
    ROWS = 3        # Number of rows in the slot machine
    COLS = 3        # Number of columns in the slot machine

    # Frequency of each symbol in the slot machine's pool
    SYMBOL_COUNT = {
        "A": 2,
        "B": 4,
        "C": 6,
        "D": 8
    }

    # Payout multiplier for each symbol if it appears on a winning line
    SYMBOL_VALUES = {
        "A": 5,
        "B": 4,
        "C": 3,
        "D": 2
    }

    def __init__(self) -> None:
        """
        Initializes a new game instance.
        - Sets up starting balance as 0.
        - Creates a SlotMachine object with predefined settings.
        """
        self.balance: int = 0 # User's current balance
        self.machine = SlotMachine(self.ROWS, self.COLS, self.SYMBOL_COUNT, self.SYMBOL_VALUES)


    def play_spin(self) -> None:
        """
        Handles a single spin round of the slot machine:
        - Asks how many lines the user wants to bet on
        - Collects bet amount per line
        - Ensures the total bet does not exceed user's available balance
        - Spins the machine and prints results
        - Checks winnings and updates balance
        """
        lines = get_number_of_slot_lines() # Ask the user how many lines they want to bet on (1-3)

        while True: # Continue prompting for a valid bet until the user has enough balance
            bet_amount = get_bet() # Ask for the bet per line
            total_bet = bet_amount * lines # Calculate total cost of the spin

            if total_bet > self.balance:
                print(f"\nYour current balance cannot meet that bet amount,\nCurrent balance: ${self.balance}.")
            else:
                break # Bet doesn't exceed user balance so exit loop and start playing.

        print(f"\nYou are betting: ${bet_amount} on {lines} lines.\nTotal bet: ${total_bet}.\n")

        # Generate the slot machine result
        columns = self.machine.spin()
        print_slot_machine(columns) # spin result

        # How much the player won and on which lines
        winnings, winning_lines = self.machine.check_winnings(columns, lines, bet_amount)

        print(f"\nYOU WON: ${winnings}")

        if winning_lines:
            print("Winning lines:", *winning_lines)
        else:
            print("No winning lines.")

        self.balance += (winnings - total_bet) # Update balance


    def run(self) -> None:
        """
        Starts and controls the main game loop:
        - Gets initial deposit amount
        - Repeats spins while the balance is above 0 or the user doesn't quit
        - Handles game over or quitting
        """
        self.balance = deposit() # Ask for initial deposit

        while True:
            if self.balance <= 0: # Check if the user has enough money to play
                print("\nGame Over. You're all out of balance.")
                print("Thank you for playing!")
                break

            print(f"Current balance: ${self.balance}")

            # Ask the user to continue playing or to quit
            user_input = input("\nPress ENTER to spin (q to quit): ").strip().lower()
            if user_input == "q":
                print(f"\nYou left with ${self.balance}.")
                break

            self.play_spin()


if __name__ == "__main__":
    game = Game()
    game.run()