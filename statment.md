# Project Design & Architecture 

This document describes how the project is organized, how files interact, and how data is stored. 

## 1. Structure 
The program uses a standard 3-module structure to keep things clean and separated: 
* **`main.py`**: Interface layer. Displays menus, grabs user choices, and routes execution. 
* **`games.py`**: Game logic. Holds game rules, scoring math, and round tracking. 
* **`data_manager.py`**: Storage handling. Reads and writes player scores to disk. 

## 2. File Overview 
```text 
[ main.py ] 
│ 
├─► [ games.py ] (runs the game and returns score) 
│ 
└─► [ data_manager.py ] (writes output) 
│ 
▼ 
[ score_history.json ] 
```

## 3. Data Format 
Player history is saved as a JSON array containing records structured as follows: 
```json
{ 
  "game": "Game Name", 
  "score": 40, 
  "timestamp": "2026-03-28 14:30:00" 
}
```

## 4. Scoring Summary 
* **Guess the Number:** Points scale based on unused attempts remaining. 
* **Word Guess:** Points scale with remaining lives upon victory. 
* **Rock, Paper, Scissors:** Flat award of 30 points for winning the best-of-three match. 
* **Tic-Tac-Toe:** Flat award of 50 points for beating the CPU. 
* **Higher or Lower:** Flat award of 40 points upon completing a 5-guess win streak.
