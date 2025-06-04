from services.logic import SlotMachine

# Sample test configuration (3x3 machine)
SYMBOLS = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

SYMBOL_VALUES = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def test_check_winnings_one_column_match() -> None:
    """
    Test case where a column has the same symbol ('A') on the first line.
    The user is betting on one line with a bet of $10.

    Expected result: winnings = 5 * 10 = 50, line 1 is a winning line.
    """
    machine = SlotMachine(3, 3, SYMBOLS, SYMBOL_VALUES)
    columns = [
        ["A", "B", "C"],
        ["A", "C", "D"],
        ["A", "D", "C"]
    ]
    winnings, lines = machine.check_winnings(columns, lines=1, bet=10)
    assert winnings == 50 # A = 5 * 10
    assert lines == [1]


def test_check_winnings_two_lines() -> None:
    """
    Test case where only two lines are bet on:
    - Line 1: all 'C' (value = 3) **WIN**
    - Line 2: mixed symbols **NO WIN**
    - Line 3: all 'D' (value = 2) **NO WIN** (Not within 2 lines bet)

    Bet per line is $10

    Expected result: (3*10) = $30, only one line is counted.
    """
    machine = SlotMachine(3, 3, SYMBOLS, SYMBOL_VALUES)
    columns = [
        ["C", "B", "D"],
        ["C", "C", "D"],
        ["C", "A", "D"]
    ]
    winnings, lines = machine.check_winnings(columns, lines=2, bet=10)
    assert winnings == 30
    assert lines == [1]



def test_check_winnings_no_match() -> None:
    """
    Test case where no row has matching symbols across all columns.

    Expected result: $0 winnings, no winning lines.
    """
    machine = SlotMachine(3, 3, SYMBOLS, SYMBOL_VALUES)
    columns = [
        ["A", "B", "C"],
        ["B", "C", "D"],
        ["C", "D", "A"]
    ]
    winnings, lines = machine.check_winnings(columns, lines=3, bet=10)
    assert winnings == 0
    assert lines == []


def test_check_winnings_multiple_lines() -> None:
    """
    Test case where multiple lines win:
    - Line 1 (row 0): all 'C' (value = 3)
    - Line 3 (row 2): all 'D' (value = 2)
    Bet is $5 per line.

    Expected result: (3*5) + (2*5) = $25, lines 1 and 3 are winning
    """
    machine = SlotMachine(3, 3, SYMBOLS, SYMBOL_VALUES)
    columns = [
        ["C", "A", "D"],
        ["C", "B", "D"],
        ["C", "B", "D"]
    ]
    winnings, lines = machine.check_winnings(columns, lines=3, bet=5)

    # C = 3 * 5, D = 2 * 5
    assert winnings == 15 + 10
    assert lines == [1, 3]


def test_check_winnings_all_lines_win() -> None:
    """
    Test case where all three lines are winning:
    - Line 1: all 'B' (value = 4)
    - Line 2: all 'C' (value = 3)
    - Line 3: all 'D' (value = 2)

    Bet is $10 per line.

    Expected result: (4*10) + (3*10) + (2*10) = $90
    """
    machine = SlotMachine(3, 3, SYMBOLS, SYMBOL_VALUES)
    columns = [
        ["B", "C", "D"],
        ["B", "C", "D"],
        ["B", "C", "D"]
    ]
    winnings, lines = machine.check_winnings(columns, lines=3, bet=10)

    assert winnings == (4*10) + (3*10) + (2*10)
    assert lines == [1,2,3]


def test_spin_structure() -> None:
    """
    Test that the `spin()` method returns a property structured 3x3 list:
    - Should have 3 columns
    - Each column should have 3 rows
    - Each symbol must be from the defined SYMBOLS dictionary
    """
    machine = SlotMachine(3, 3, SYMBOLS, SYMBOL_VALUES)
    columns = machine.spin()

    assert isinstance(columns, list)
    assert len(columns) == 3 # Three columns
    for col in columns:
        assert isinstance(col, list)
        assert len(col) == 3 # Three rows per column
        for symbol in col:
            assert symbol in SYMBOLS.keys()