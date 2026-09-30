# Terminal Mini-Games Hub

A simple Python project containing five text-based mini-games played in the command line.

## Project Structure
- **`main.py`**: Handles menu navigation and running the selected game.
- **`games.py`**: Contains the logic and loops for each of the 5 games.
- **`data_manager.py`**: Saves and loads scores to a local JSON file.

## Games
1. **Guess the Number**: Find the random number within 7 tries.
2. **Word Guess**: Guess a secret word one letter at a time.
3. **Rock, Paper, Scissors**: Play a best-of-three match against the computer.
4. **Tic-Tac-Toe**: Standard 3x3 game against a simple CPU opponent.
5. **Higher or Lower**: Get 5 correct guesses in a row on whether the next number is higher or lower.

## Running the App
Make sure you have Python 3 installed. Open your terminal in this folder and run:

```bash
python main.py