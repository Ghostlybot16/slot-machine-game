from services.ui import deposit, get_number_of_slot_lines, get_bet, print_slot_machine

# --- deposit() tests ---

def test_deposit_valid(monkeypatch) -> None:
    """
    Test deposit() with a single valid numeric input.

    Expected output: The entered integer value of 200.
    """
    monkeypatch.setattr("builtins.input", lambda _: "200")
    result = deposit()
    assert result == 200


def test_deposit_invalid_then_valid(monkeypatch) -> None:
    """
    Test deposit() with a series of invalid inputs followed by a valid one.

    Expected output: Should return 50.
    """
    inputs = iter(["-5", "abc", "0", "50"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = deposit()
    assert result == 50


# --- get_number_of_slot_lines() tests ---

def test_get_number_of_slot_lines_valid(monkeypatch) -> None:
    """
    Test get_number_of_slot_lines() with a valid number in range (1-3).

    Expected output: 3
    """
    monkeypatch.setattr("builtins.input", lambda _: "3")
    result = get_number_of_slot_lines()
    assert result == 3

def test_get_number_of_slot_lines_invalid_then_valid(monkeypatch) -> None:
    """
    Test get_number_of_slot_lines() with invalid inputs followed by valid input.

    Expected output: Should return 2.
    """
    inputs = iter(["0", "abc", "4", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_number_of_slot_lines()
    assert result == 2

def test_get_number_of_slot_lines_min(monkeypatch) -> None:
    """
    Test get_number_of_slot_lines() with the minimum allowed value (1).

    Expected output: 1
    """
    monkeypatch.setattr("builtins.input", lambda _: "1")
    result = get_number_of_slot_lines()
    assert result == 1

# --- get_bet() tests ___

def test_get_bet_valid(monkeypatch) -> None:
    """
    Test get_bet() with a valid input in range.

    Expected output: 25
    """
    monkeypatch.setattr("builtins.input", lambda _: "25")
    result = get_bet()
    assert result == 25


def test_get_bet_invalid_then_valid(monkeypatch) -> None:
    """
    Test get_bet() with a series of invalid inputs followed by a valid input.

    Expected output: Should return 10
    """
    inputs = iter(["0", "999", "abc", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_bet()
    assert result == 10

def test_get_bet_minimum(monkeypatch) -> None:
    """
    Test get_bet() with the minimum valid value (1).

    Expected output: 1
    """
    monkeypatch.setattr("builtins.input", lambda _: "1")
    result = get_bet()
    assert result == 1

def test_get_bet_maximum(monkeypatch) -> None:
    """
    Test get_bet() with the maximum valid value (100)

    Expected output: 100
    """
    monkeypatch.setattr("builtins.input", lambda _: "100")
    result = get_bet()
    assert result == 100

# --- print_slot_machine() test (basic output check) ---

def test_print_slot_machine(capsys) -> None:
    """
    Test print_slot_machine() by checking output formatting.
    It should print rows with correct alignment and pipe separators.
    """
    columns = [
        ["A", "B", "C"],
        ["A", "C", "D"],
        ["A", "D", "C"]
    ]
    print_slot_machine(columns)
    captured = capsys.readouterr()
    assert "A | A | A" in captured.out
    assert "B | C | D" in captured.out

def test_print_slot_machine_row_count(capsys) -> None:
    """
    Ensure the number of printed rows matches the slot machine layout.
    """
    columns = [
        ["X", "Y", "Z"],
        ["X", "Y", "Z"],
        ["X", "Y", "Z"]
    ]
    print_slot_machine(columns)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")
    assert len(output_lines) == 3 # 3 rows expected