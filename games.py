import random

def guess_number():
    secret = random.randint(1, 100)
    max_tries = 7
    print("I'm thinking of a number between 1 and 100.")
    
    for attempt in range(1, max_tries + 1):
        try:
            guess = int(input(f"Attempt {attempt}/{max_tries} - Take a guess: "))
        except ValueError:
            print("Enter a whole number.")
            continue
            
        if guess < secret:
            print("Too low!")
        elif guess > secret:
            print("Too high!")
        else:
            print(f"Nice! You got it in {attempt} tries.")
            score = (max_tries - attempt + 1) * 10
            return True, score
            
    print(f"Out of tries! The number was {secret}.")
    return False, 0


def word_guess():
    words = ["python", "programming", "developer", "terminal", "script", "code"]
    word = random.choice(words)
    guessed = set()
    lives = 6
    
    print("Guess the secret word letter by letter!")
    
    while lives > 0:
        display = "".join([char if char in guessed else "_" for char in word])
        print(f"\nWord: {display}")
        print(f"Lives left: {lives}")
        
        if "_" not in display:
            print("You guessed it!")
            return True, lives * 15
            
        guess = input("Guess a letter: ").lower().strip()
        if len(guess) != 1 or not guess.isalpha():
            print("Please pick a single letter.")
            continue
            
        if guess in guessed:
            print("You already tried that letter.")
            continue
            
        guessed.add(guess)
        if guess in word:
            print("Got one!")
        else:
            print("Nope, wrong letter.")
            lives -= 1
            
    print(f"\nGame over! The word was: {word}")
    return False, 0


def rock_paper_scissors():
    moves = ["rock", "paper", "scissors"]
    p_score, c_score = 0, 0
    
    print("Best 2 out of 3 against the computer!")
    
    while p_score < 2 and c_score < 2:
        print(f"\nScore -> You: {p_score} | CPU: {c_score}")
        user = input("Choose rock, paper, or scissors: ").lower().strip()
        if user not in moves:
            print("Invalid choice, try again.")
            continue
            
        cpu = random.choice(moves)
        print(f"Computer picked: {cpu}")
        
        if user == cpu:
            print("Tie round!")
        elif (user == "rock" and cpu == "scissors") or \
             (user == "paper" and cpu == "rock") or \
             (user == "scissors" and cpu == "paper"):
            print("You won this round!")
            p_score += 1
        else:
            print("Computer took this round.")
            c_score += 1
            
    if p_score == 2:
        print("\nYou won the match!")
        return True, 30
    else:
        print("\nComputer won the match!")
        return False, 0


def tic_tac_toe():
    board = [" "] * 9
    
    def draw():
        print(f"\n {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} ")
        
    def check_winner(b, mark):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[w[0]] == b[w[1]] == b[w[2]] == mark for w in wins)

    print("Tic-Tac-Toe! Board slots are numbered 1 through 9.")
    draw()
    
    for turn in range(9):
        if turn % 2 == 0:
            move = -1
            while move not in range(9) or board[move] != " ":
                try:
                    move = int(input("\nPick a slot (1-9): ")) - 1
                    if board[move] != " ":
                        print("Slot taken, pick another.")
                        move = -1
                except (ValueError, IndexError):
                    print("Invalid slot. Pick an open number from 1 to 9.")
                    move = -1
            board[move] = "X"
            if check_winner(board, "X"):
                draw()
                print("\nYou won!")
                return True, 50
        else:
            open_slots = [i for i, val in enumerate(board) if val == " "]
            move = random.choice(open_slots)
            board[move] = "O"
            print(f"\nComputer placed O at slot {move + 1}")
            if check_winner(board, "O"):
                draw()
                print("\nComputer won!")
                return False, 0
                
        draw()
        if " " not in board:
            print("\nDraw game!")
            return False, 0


def higher_or_lower():
    current = random.randint(1, 100)
    streak = 0
    target = 5
    
    print(f"Get {target} correct higher/lower guesses in a row to win!")
    
    while streak < target:
        print(f"\nCurrent number: {current}")
        user_guess = input("Will the next number be (H)igher or (L)ower? ").lower().strip()
        if user_guess not in ['h', 'l']:
            print("Enter 'h' for higher or 'l' for lower.")
            continue
            
        nxt = random.randint(1, 100)
        while nxt == current:
            nxt = random.randint(1, 100)
            
        print(f"Next number was: {nxt}")
        
        went_up = nxt > current
        if (user_guess == 'h' and went_up) or (user_guess == 'l' and not went_up):
            streak += 1
            print(f"Right! Streak: {streak}/{target}")
            current = nxt
        else:
            print(f"Wrong! Streak reset. You made it to {streak}.")
            return False, 0
            
    print("\nStreak completed!")
    return True, 40