import random
from typing import List, Dict, Tuple

def check_winnings(columns: List[List[str]], lines: int, bet: int, values: Dict[str, int]) -> Tuple[int, List[int]]:
    """
    Check for winning lines and calculate total winnings.

    Args:
        columns (List[List[str]]): Columns of the slot machine.
        lines (int): Number of lines the user is betting on.
        bet (int): The bet amount per line.
        values (dict): Payout multiplier for each symbol.

    Returns:
        Tuple[int, List[int]]: Total winnings and a list of winning line numbers.
    """
    winnings = 0
    winning_lines = []

    for line in range(lines): # Loop through every row
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check: # If symbols are not the same then break out of the loop and check the next line
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines




def get_slot_machine_spin(rows: int, cols: int, symbols: Dict[str, int]) -> List[List[str]]:
    """
    Simulate a spin of the slot machine.

    Args:
         rows (int): Number of rows in the machine.
         cols (int): Number of columns in the machine.
         symbols (Dict[str, int]): Pool of symbols and their occurrence frequency.

     Returns:
        List[List[str]]: A list of columns, each contains row values.
    """

    all_symbols = []

    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:] # Create a copy of the all_symbols list
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value) # Remove the symbol so it doesn't get chosen again
            column.append(value) # Add the value to the column

        columns.append(column) # Add the column to the column list

    return columns