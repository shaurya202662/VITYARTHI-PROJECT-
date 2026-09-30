import sys
import games
import data_manager

def show_menu():
    print("\n" + "=" * 35)
    print("      PYTHON MINI-GAMES      ")
    print("=" * 35)
    print("1. Guess the Number")
    print("2. Word Guess")
    print("3. Rock, Paper, Scissors")
    print("4. Tic-Tac-Toe")
    print("5. Higher or Lower")
    print("6. High Scores")
    print("7. Exit")
    print("=" * 35)

def main():
    data_manager.init_db()
    
    while True:
        show_menu()
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            won, score = games.guess_number()
            if won:
                data_manager.save_score("Guess the Number", score)
                
        elif choice == '2':
            won, score = games.word_guess()
            if won:
                data_manager.save_score("Word Guess", score)
                
        elif choice == '3':
            won, score = games.rock_paper_scissors()
            if won:
                data_manager.save_score("Rock, Paper, Scissors", score)
                
        elif choice == '4':
            won, score = games.tic_tac_toe()
            if won:
                data_manager.save_score("Tic-Tac-Toe", score)
                
        elif choice == '5':
            won, score = games.higher_or_lower()
            if won:
                data_manager.save_score("Higher or Lower", score)
                
        elif choice == '6':
            data_manager.show_scores()
            
        elif choice == '7':
            print("\nThanks for playing!")
            sys.exit()
            
        else:
            print("\nInvalid choice. Enter a number between 1 and 7.")
            
        input("\nPress Enter to go back to the menu...")

if __name__ == "__main__":
    main()