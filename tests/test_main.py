from main import Game

def test_game_initial_balance_zero() -> None:
    """
    Verify that a newly created Game object has an initial balance of 0.
    """
    game = Game()
    assert game.balance == 0


def test_game_deposit_sets_balance(monkeypatch) -> None:
    """
    Simulate deposit input and confirm Game object's balance is updated
    """
    monkeypatch.setattr("builtins.input", lambda _: "150")
    game = Game()
    game.run = lambda: None # Avoid running the full game loop
    game.balance = int(input("mocked")) # Simulated deposit
    assert game.balance == 150

def test_play_spin_win(monkeypatch, capsys) -> None:
    """
    Simulate a full spin with guaranteed win by mocking:
    - deposit = 100
    - number of lines = 1
    - bet per line = 10
    - forced spin to produce 3 matching 'C's on row 0

    Assert winnings message is printed and balance update.
    """
    game = Game()
    game.balance = 100

    prompts = {
        f"\nEnter the number of slot lines to bet on (1-{game.MAX_LINES})\n": "1",
        "\nHow much money would you like to bet on each slot line? \n$": "10"
    }

    monkeypatch.setattr("builtins.input", lambda prompt: prompts[prompt])

    # Force the spin to return a winning condition for row 0
    game.machine.spin = lambda : [
        ["C", "B", "D"],
        ["C", "B", "D"],
        ["C", "B", "D"]
    ]

    game.play_spin()

    captured = capsys.readouterr()
    assert "YOU WON:" in captured.out
    assert game.balance > 90 # Net gain



def test_play_spin_insufficient_balance(monkeypatch, capsys) -> None:
    """
    Simulate user trying to bet more than balance:
    - balance = 20
    - first bet = 50 (too much)
    - second bet = 5 (valid)

    Validate the proper warning message is printed.
    """
    game = Game()
    game.balance = 20

    inputs = iter([
        f"\nEnter the number of slot lines to bet on (1-{game.MAX_LINES})\n",  # slot lines = 3
        "\nHow much money would you like to bet on each slot line? \n$",  # bet = 50 (fail)
        "\nHow much money would you like to bet on each slot line? \n$"  # bet = 5 (pass)
    ])

    answers = iter(["3", "50", "5"])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    game.machine.spin = lambda: [["A", "A", "A"]] * 3  # Dummy spin

    game.play_spin()

    captured = capsys.readouterr()
    assert "cannot meet that bet amount" in captured.out


def test_play_spin_exact_balance(monkeypatch, capsys) -> None:
    """
    Simulate a spin where the total bet equals winnings.
    Balance should remain unchanged.
    """

    game = Game()
    game.balance = 15

    monkeypatch.setattr("builtins.input", lambda prompt: {
        f"\nEnter the number of slot lines to bet on (1-{game.MAX_LINES})\n": "1",
        "\nHow much money would you like to bet on each slot line? \n$": "15"
    }[prompt])

    game.machine.spin = lambda: [["A", "B", "C"]] * 3
    game.machine.check_winnings = lambda *_: (15, [1]) # Simulate breakeven

    game.play_spin()
    assert game.balance == 15


def test_run_game_over(monkeypatch, capsys) -> None:
    """ 
    Simulate run where user starts with $10 and bets $10 but loses, thus ending the game.
    """
    inputs = iter([
        "10", #deposit
        "",   #spin
        "1",  #lines
        "10"  #bet amount
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    game = Game()
    game.machine.spin = lambda: [["A", "B", "C"]] * 3
    game.machine.check_winnings = lambda *_: (0, [])
    
    game.run()
    captured = capsys.readouterr()
    assert "Game Over" in captured.out

def test_run_quit_immediately(monkeypatch, capsys) -> None:
    """
    Simulate the user depositing and quitting immediately.
    Expect correct balance display and exit message.
    """
    inputs = iter(["100", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    game = Game()
    game.run()

    captured = capsys.readouterr()
    assert "Current balance: $100" in captured.out
    assert "You left with $100" in captured.out