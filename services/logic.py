import random
from typing import List, Dict, Tuple


class SlotMachine:
    """
    A class that represents a slot machine with spinning and winnings logic.
    """

    def __init__(self, rows: int, cols: int, symbols: Dict[str, int], symbol_values: Dict[str, int]) -> None:
        """
        Initialize the slot machine with configuration.

        Args:
            rows (int): Number of rows in the machine.
            cols (int): Number of columns in the machine.
            symbols (Dict[str, int]): Symbol with their frequency.
            symbol_values (Dict[str, int]): Payout multiplier per symbol.
        """
        self.rows = rows
        self.cols = cols
        self.symbols = symbols
        self.symbol_values = symbol_values


    def spin(self) -> List[List[str]]:
        """
        Simulates a spin of the slot machine.

        Returns:
             List[List[str]]: A list of columns, each containing row symbols.
        """
        all_symbols = []
        for symbol, count in self.symbols.items():
            for _ in range(count):
                all_symbols.append(symbol)

        all_columns: List[List[str]] = [] # Holds all the columns that will make up the spin result

        # Loop once for each column
        for _ in range(self.cols):
            column : List[str] = [] # Individual column
            current_symbols = all_symbols[:]  # Create a copy of the full symbol pool

            # For each row in this column, randomly choose a symbol
            for _ in range(self.rows):
                value = random.choice(current_symbols) # Randomly pick a symbol
                current_symbols.remove(value)  # Remove the symbol so it doesn't get chosen again
                column.append(value)  # Add the chosen symbol to this column

            all_columns.append(column)  # Add the completed column to the column list

        # Return the full slot machine result (list of columns with row values)
        return all_columns


    def check_winnings(self, columns: List[List[str]], lines: int, bet: int) -> Tuple[int, List[int]]:
        """
        Calculate total winnings and winning lines based on the slot result.

        Args:
            columns (List[List[str]]): Columns of the slot machine.
            lines (int): Number of lines the user is betting on.
            bet (int): The bet amount per line.

        Returns:
            Tuple[int, List[int]]: Total winnings and a list of winning line numbers.
        """
        winnings = 0
        winning_lines = [] # Keeps track of which lines (rows) won

        for line in range(lines): # Loop through every row up to the number of lines the user bet on
            symbol = columns[0][line]

            # Check if all the columns have the same symbol in this row
            for column in columns:
                if column[line] != symbol: # If symbols are not the same then break out of the loop and check the next line
                    break
            else: # If the loop didn't break, all symbols matched, therefore a win.
                winnings += self.symbol_values[symbol] * bet # Multiply symbol value by bet amount
                winning_lines.append(line + 1)

        # Return total money won and which lines were winners
        return winnings, winning_lines