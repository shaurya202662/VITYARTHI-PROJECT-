import json
import os
from datetime import datetime

DB_FILE = "score_history.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def save_score(game_name, score):
    data = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

    entry = {
        "game": game_name,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(entry)

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {score} pts for {game_name}!")

def show_scores():
    if not os.path.exists(DB_FILE):
        print("\nNo score history found.")
        return
        
    with open(DB_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        
    if not data:
        print("\nNo scores recorded yet!")
        return
        
    print("\n" + "=" * 45)
    print("             SCORE HISTORY             ")
    print("=" * 45)
    print(f"{'Game':<22} | {'Score':<6} | {'Date'}")
    print("-" * 45)
    for entry in reversed(data[-10:]):
        print(f"{entry['game']:<22} | {entry['score']:<6} | {entry['timestamp']}")
    print("=" * 45)