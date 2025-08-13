import random


def get_valid_guess(input_func=input, print_func=print):
    """Prompts for a valid integer guess, re-prompting on invalid input."""
    while True:
        user_input = input_func("Enter your guess: ").strip()
        try:
            return int(user_input)
        except ValueError:
            print_func("Invalid input. Please enter an integer.")


def play_round(input_func=input, print_func=print):
    """Plays one round of the guessing game and returns the number of attempts."""
    secret = random.randint(1, 100)
    attempts = 0
    
    print_func("I'm thinking of a number between 1 and 100.")
    
    while True:
        guess = get_valid_guess(input_func, print_func)
        attempts += 1
        
        if guess < secret:
            print_func("Too low!")
        elif guess > secret:
            print_func("Too high!")
        else:
            print_func(f"Correct! You got it in {attempts} attempts.")
            return attempts


def ask_play_again(input_func=input, print_func=print):
    """Asks if the player wants to play again and returns True/False."""
    while True:
        response = input_func("Play again? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print_func("Please enter 'y' for yes or 'n' for no.")


def main(input_func=input, print_func=print):
    """Main game loop controlling multiple rounds."""
    print_func("Welcome to Number Guessing!")
    
    while True:
        play_round(input_func, print_func)
        
        if not ask_play_again(input_func, print_func):
            print_func("Thanks for playing. Goodbye!")
            break
        print_func()


if __name__ == "__main__":
    main()