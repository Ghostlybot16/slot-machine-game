from typing import List

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

def print_slot_machine(columns: List[List[str]]) -> None:
    """
    Display the slot machine grid in the terminal.

    Args:
         columns (List[List[str]]): The columns of the slot machine.
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1: # If not last column of the slot machine add the pipe symbol
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print() # New line for spacing



# Function to collect user input for deposit value
def deposit() -> int:
    """
    Prompt the user for a deposit amount and validate it.

    Returns:
         int: The validated deposit amount.
    """
    while True: # while loop to continually ask the user until a valid amount has been input

        amount = input("How much would you like to deposit?\n$")

        if amount.isdigit(): # Check if the input is a valid number
            amount = int(amount) # convert string to int

            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.\n") # Let the user know that they entered an amount less than 0
        else:
            print("Please enter a positive integer number.\n") # Ask the user to enter a digit



# Function to get the number of lines
def get_number_of_slot_lines() -> int:
    """
    Prompt the user to enter how many lines they want to bet on.

    Returns:
        int: Number of lines to bet on.
    """
    while True:
        slot_lines = input(f"\nEnter the number of slot lines to bet on (1-{str(MAX_LINES)})\n")

        if slot_lines.isdigit():
            slot_lines = int(slot_lines)

            if 1 <= slot_lines <= MAX_LINES:
                return slot_lines
            else:
                print(f"Enter a valid number of slot lines (1-{str(MAX_LINES)})\n")
        else:
            print("Please enter a positive integer number\n")




def get_bet() -> int:
    """
    Prompt the user for the amount to bet on each line.

    Returns:
         int: Validated bet amount per line.
    """
    while True:
        bet_amount = input("\nHow much would you like to bet on each slot line? \n$")

        if bet_amount.isdigit():
            bet_amount = int(bet_amount)

            if MIN_BET <= bet_amount <= MAX_BET:
                return bet_amount
            else:
                print(f"Bet amount must be between {MIN_BET} - {MAX_BET}.\n")
        else:
            print("Please enter a positive integer number\n")

