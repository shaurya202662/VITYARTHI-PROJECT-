"""Tests for the Terminal Mini-Games Hub.

Run from the project folder with:
    python -m unittest -v
(or `pytest`, if you have it installed)

The tests never touch your real score_history.json: scores are written
to a temporary folder, and all user input / randomness is faked.
"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import data_manager
import games
import main


def run_quietly(func, *args):
    """Run a function while hiding its print() output."""
    with redirect_stdout(io.StringIO()):
        return func(*args)


def capture(func, *args):
    """Run a function and return everything it printed."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args)
    return buf.getvalue()


# --------------------------------------------------------------------------
# data_manager.py
# --------------------------------------------------------------------------
class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "scores.json")
        patcher = patch.object(data_manager, "DB_FILE", self.db)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def read_db(self):
        with open(self.db) as f:
            return json.load(f)

    def test_init_db_creates_empty_list(self):
        data_manager.init_db()
        self.assertEqual(self.read_db(), [])

    def test_init_db_keeps_existing_data(self):
        with open(self.db, "w") as f:
            json.dump([{"game": "X", "score": 1, "timestamp": "t"}], f)
        data_manager.init_db()
        self.assertEqual(len(self.read_db()), 1)

    def test_save_score_stores_all_fields(self):
        run_quietly(data_manager.save_score, "Word Guess", 90)
        entry = self.read_db()[0]
        self.assertEqual(entry["game"], "Word Guess")
        self.assertEqual(entry["score"], 90)
        self.assertIn("timestamp", entry)

    def test_save_score_appends(self):
        run_quietly(data_manager.save_score, "A", 10)
        run_quietly(data_manager.save_score, "B", 20)
        self.assertEqual([e["game"] for e in self.read_db()], ["A", "B"])

    def test_save_score_recovers_from_corrupted_file(self):
        with open(self.db, "w") as f:
            f.write("{ not valid json")
        run_quietly(data_manager.save_score, "A", 10)
        self.assertEqual(len(self.read_db()), 1)

    def test_show_scores_when_file_missing(self):
        out = capture(data_manager.show_scores)
        self.assertIn("No score history found", out)

    def test_show_scores_when_empty(self):
        data_manager.init_db()
        out = capture(data_manager.show_scores)
        self.assertIn("No scores recorded yet", out)

    def test_show_scores_when_file_corrupted(self):
        with open(self.db, "w") as f:
            f.write("oops")
        out = capture(data_manager.show_scores)
        self.assertIn("No scores recorded yet", out)

    def test_show_scores_only_last_10_newest_first(self):
        for i in range(12):
            run_quietly(data_manager.save_score, f"Game{i:02d}", i)
        out = capture(data_manager.show_scores)
        self.assertNotIn("Game00", out)      # too old
        self.assertNotIn("Game01", out)      # too old
        self.assertIn("Game02", out)         # oldest one still shown
        self.assertLess(out.index("Game11"), out.index("Game02"))


# --------------------------------------------------------------------------
# games.py
# --------------------------------------------------------------------------
class TestGuessNumber(unittest.TestCase):
    @patch("games.random.randint", return_value=50)
    def test_win_first_try_gives_70(self, _):
        with patch("builtins.input", side_effect=["50"]):
            self.assertEqual(run_quietly(games.guess_number), (True, 70))

    @patch("games.random.randint", return_value=50)
    def test_win_third_try_gives_50(self, _):
        with patch("builtins.input", side_effect=["10", "90", "50"]):
            self.assertEqual(run_quietly(games.guess_number), (True, 50))

    @patch("games.random.randint", return_value=50)
    def test_win_last_try_gives_10(self, _):
        with patch("builtins.input", side_effect=["1"] * 6 + ["50"]):
            self.assertEqual(run_quietly(games.guess_number), (True, 10))

    @patch("games.random.randint", return_value=50)
    def test_lose_after_seven_tries(self, _):
        with patch("builtins.input", side_effect=["1"] * 7):
            self.assertEqual(run_quietly(games.guess_number), (False, 0))

    @patch("games.random.randint", return_value=50)
    def test_hints_are_correct(self, _):
        with patch("builtins.input", side_effect=["10", "90", "50"]):
            out = capture(games.guess_number)
        self.assertIn("Too low!", out)
        self.assertIn("Too high!", out)

    @patch("games.random.randint", return_value=50)
    def test_non_number_does_not_crash(self, _):
        with patch("builtins.input", side_effect=["abc", "50"]):
            won, _score = run_quietly(games.guess_number)
        self.assertTrue(won)


class TestWordGuess(unittest.TestCase):
    @patch("games.random.choice", return_value="code")
    def test_win_with_all_lives_gives_90(self, _):
        with patch("builtins.input", side_effect=list("code")):
            self.assertEqual(run_quietly(games.word_guess), (True, 90))

    @patch("games.random.choice", return_value="code")
    def test_win_after_two_mistakes_gives_60(self, _):
        with patch("builtins.input", side_effect=["x", "z"] + list("code")):
            self.assertEqual(run_quietly(games.word_guess), (True, 60))

    @patch("games.random.choice", return_value="code")
    def test_lose_after_six_wrong_letters(self, _):
        with patch("builtins.input", side_effect=list("xyzqwv")):
            self.assertEqual(run_quietly(games.word_guess), (False, 0))

    @patch("games.random.choice", return_value="code")
    def test_invalid_and_repeated_input_cost_no_lives(self, _):
        inputs = ["", "ab", "1", "c", "c"] + list("ode")
        with patch("builtins.input", side_effect=inputs):
            self.assertEqual(run_quietly(games.word_guess), (True, 90))

    @patch("games.random.choice", return_value="code")
    def test_uppercase_letters_are_accepted(self, _):
        with patch("builtins.input", side_effect=list("CODE")):
            self.assertEqual(run_quietly(games.word_guess), (True, 90))


class TestRockPaperScissors(unittest.TestCase):
    def test_player_wins_two_rounds(self):
        with patch("games.random.choice", side_effect=["scissors", "rock"]), \
             patch("builtins.input", side_effect=["rock", "paper"]):
            self.assertEqual(run_quietly(games.rock_paper_scissors), (True, 30))

    def test_cpu_wins_two_rounds(self):
        with patch("games.random.choice", side_effect=["paper", "rock"]), \
             patch("builtins.input", side_effect=["rock", "scissors"]):
            self.assertEqual(run_quietly(games.rock_paper_scissors), (False, 0))

    def test_tie_does_not_change_score(self):
        cpu = ["rock", "scissors", "scissors"]
        with patch("games.random.choice", side_effect=cpu), \
             patch("builtins.input", side_effect=["rock", "rock", "rock"]):
            self.assertEqual(run_quietly(games.rock_paper_scissors), (True, 30))

    def test_invalid_choice_is_ignored(self):
        with patch("games.random.choice", side_effect=["scissors", "scissors"]), \
             patch("builtins.input", side_effect=["banana", "rock", "rock"]):
            self.assertEqual(run_quietly(games.rock_paper_scissors), (True, 30))

    def test_every_winning_combination(self):
        for user, cpu in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]:
            with self.subTest(user=user, cpu=cpu):
                with patch("games.random.choice", side_effect=[cpu, cpu]), \
                     patch("builtins.input", side_effect=[user, user]):
                    self.assertEqual(run_quietly(games.rock_paper_scissors), (True, 30))


class TestTicTacToe(unittest.TestCase):
    """The CPU is faked so it always takes the LAST open slot."""

    @staticmethod
    def cpu_takes_last(open_slots):
        return open_slots[-1]

    def test_player_wins_top_row(self):
        with patch("games.random.choice", side_effect=self.cpu_takes_last), \
             patch("builtins.input", side_effect=["1", "2", "3"]):
            self.assertEqual(run_quietly(games.tic_tac_toe), (True, 50))

    def test_cpu_wins(self):
        with patch("games.random.choice", side_effect=self.cpu_takes_last), \
             patch("builtins.input", side_effect=["1", "4", "2"]):
            self.assertEqual(run_quietly(games.tic_tac_toe), (False, 0))

    def test_draw_game_gives_no_points(self):
        # Final board:  X O X / X O O / O X X
        cpu_moves = [1, 4, 5, 6]
        with patch("games.random.choice", side_effect=cpu_moves), \
             patch("builtins.input", side_effect=["1", "3", "4", "8", "9"]):
            out = capture(games.tic_tac_toe)
        self.assertIn("Draw game!", out)

    def test_taken_and_invalid_slots_are_rejected(self):
        # "1" is taken by the player; "0", "10" and "abc" are invalid
        inputs = ["1", "1", "0", "10", "abc", "2", "3"]
        with patch("games.random.choice", side_effect=self.cpu_takes_last), \
             patch("builtins.input", side_effect=inputs):
            out = capture(games.tic_tac_toe)
        self.assertIn("Slot taken", out)
        self.assertIn("Invalid slot", out)
        self.assertIn("You won!", out)


class TestHigherOrLower(unittest.TestCase):
    def test_win_after_five_correct_guesses(self):
        numbers = [50, 60, 70, 80, 90, 95]        # start + 5 next numbers
        with patch("games.random.randint", side_effect=numbers), \
             patch("builtins.input", side_effect=["h"] * 5):
            self.assertEqual(run_quietly(games.higher_or_lower), (True, 40))

    def test_lower_guess_works(self):
        numbers = [50, 40, 30, 20, 10, 5]
        with patch("games.random.randint", side_effect=numbers), \
             patch("builtins.input", side_effect=["l"] * 5):
            self.assertEqual(run_quietly(games.higher_or_lower), (True, 40))

    def test_wrong_guess_ends_game(self):
        with patch("games.random.randint", side_effect=[50, 30]), \
             patch("builtins.input", side_effect=["h"]):
            self.assertEqual(run_quietly(games.higher_or_lower), (False, 0))

    def test_invalid_input_is_ignored(self):
        numbers = [50, 60, 70, 80, 90, 95]
        with patch("games.random.randint", side_effect=numbers), \
             patch("builtins.input", side_effect=["x", ""] + ["h"] * 5):
            self.assertEqual(run_quietly(games.higher_or_lower), (True, 40))

    def test_same_number_is_rerolled(self):
        numbers = [50, 50, 60, 70, 80, 90, 95]   # the repeated 50 must be skipped
        with patch("games.random.randint", side_effect=numbers), \
             patch("builtins.input", side_effect=["h"] * 5):
            self.assertEqual(run_quietly(games.higher_or_lower), (True, 40))


# --------------------------------------------------------------------------
# main.py (menu)
# --------------------------------------------------------------------------
class TestMainMenu(unittest.TestCase):
    def run_menu(self, inputs):
        """Run main() with fake keyboard input until the user exits."""
        with patch("builtins.input", side_effect=inputs), \
             redirect_stdout(io.StringIO()) as buf:
            with self.assertRaises(SystemExit):
                main.main()
        return buf.getvalue()

    @patch("main.data_manager.init_db")
    @patch("main.data_manager.save_score")
    def test_win_is_saved(self, save, _init):
        with patch("main.games.guess_number", return_value=(True, 70)):
            self.run_menu(["1", "", "7"])
        save.assert_called_once_with("Guess the Number", 70)

    @patch("main.data_manager.init_db")
    @patch("main.data_manager.save_score")
    def test_loss_is_not_saved(self, save, _init):
        with patch("main.games.word_guess", return_value=(False, 0)):
            self.run_menu(["2", "", "7"])
        save.assert_not_called()

    @patch("main.data_manager.init_db")
    @patch("main.data_manager.save_score")
    def test_each_menu_option_saves_under_correct_name(self, save, _init):
        options = {
            "1": ("guess_number", "Guess the Number"),
            "2": ("word_guess", "Word Guess"),
            "3": ("rock_paper_scissors", "Rock, Paper, Scissors"),
            "4": ("tic_tac_toe", "Tic-Tac-Toe"),
            "5": ("higher_or_lower", "Higher or Lower"),
        }
        for choice, (func, name) in options.items():
            with self.subTest(choice=choice):
                save.reset_mock()
                with patch(f"main.games.{func}", return_value=(True, 10)):
                    self.run_menu([choice, "", "7"])
                save.assert_called_once_with(name, 10)

    @patch("main.data_manager.init_db")
    @patch("main.data_manager.show_scores")
    def test_option_6_shows_scores(self, show, _init):
        self.run_menu(["6", "", "7"])
        show.assert_called_once()

    @patch("main.data_manager.init_db")
    def test_invalid_choice_shows_message(self, _init):
        out = self.run_menu(["9", "", "7"])
        self.assertIn("Invalid choice", out)

    @patch("main.data_manager.init_db")
    def test_exit_says_goodbye(self, _init):
        out = self.run_menu(["7"])
        self.assertIn("Thanks for playing!", out)


if __name__ == "__main__":
    unittest.main()
