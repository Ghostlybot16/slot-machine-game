from services.logic import get_slot_machine_spin, check_winnings
from services.ui import deposit, get_bet, get_number_of_slot_lines, print_slot_machine

MAX_LINES = 3 # Constant value

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_values = { # Score multiplier
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def spin(balance: int) -> int:
    """
    Runs a single round of the slot machine spin with user input and updates balance.

    Args:
         balance (int): User's current balance.

    Returns:
        int: Net change in balance (winnings - total bet).
    """
    slot_lines_to_bet = get_number_of_slot_lines()

    while True:
        bet_amount = get_bet()
        total_bet_amount = bet_amount * slot_lines_to_bet

        if total_bet_amount > balance:
            print(f"\nYour current balance cannot meet that bet amount,\nCurrent balance: ${balance}.")
        else:
            break

    print(
        f"\nYou are betting: ${bet_amount} on {slot_lines_to_bet} lines.\nTotal bet is equal to: ${total_bet_amount}.\n")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, slot_lines_to_bet, bet_amount, symbol_values)
    print(f"YOU WON ${winnings}.")
    print(f"You won on lines:", *winning_lines)

    return winnings - total_bet_amount # How much was won or lost from the spin



def main() -> None:
    """
    Entry point of the slot machine game.
    Runs the slot machine game loop.
    Handles user balance, re-spinning and quitting the game
    """
    balance = deposit()

    while True:
        if balance <= 0:
            print("\nGame Over. You're all out of balance.")
            print("Thank you for playing!")
            break

        print(f"Current balance is: ${balance}.\n")
        user_answer = input("Press Enter to spin (q to quit).")

        if user_answer.lower == "q":
            print(f"\nYou left with ${balance}")
            break

        balance += spin(balance)

if __name__ == "__main__":
    main()