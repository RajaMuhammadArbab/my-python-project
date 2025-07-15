import random
import sys
import json
import os


leaderboard = []
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    global leaderboard
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            leaderboard = json.load(file)
    else:
        leaderboard = []

def save_leaderboard():
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)


def print_instructions():
    print("\nWelcome to 'Guess the Number'!")
    print("Your goal is to guess the randomly chosen number in as few attempts as possible.")
    print("Use hints wisely to guess the number correctly!\n")

def settings_menu():
    while True:
        print("\nSettings Menu:")
        print("1. Select Difficulty Level")
        print("2. Set Custom Range")
        print("3. View Leaderboard")
        print("4. Exit Settings")
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            return get_difficulty_level()
        elif choice == '2':
            return set_custom_range()
        elif choice == '3':
            view_leaderboard()
        elif choice == '4':
            return None
        else:
            print("Invalid choice. Try again.")

def get_difficulty_level():
    print("\nSelect Difficulty:")
    print("1. Easy (1-10, 5 attempts)")
    print("2. Medium (1-50, 7 attempts)")
    print("3. Hard (1-100, 10 attempts)")
    choice = input("Enter choice (1-3): ")

    if choice == '1':
        return 1, 10, 5
    elif choice == '2':
        return 1, 50, 7
    elif choice == '3':
        return 1, 100, 10
    else:
        print("Invalid choice. Defaulting to Easy.")
        return 1, 10, 5

def set_custom_range():
    try:
        start = int(input("Enter start of range: "))
        end = int(input("Enter end of range: "))
        attempts = int(input("Enter number of attempts: "))

        if start >= end or attempts <= 0:
            print("Invalid input. Try again.")
            return set_custom_range()
        return start, end, attempts
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return set_custom_range()

def view_leaderboard():
    print("\nLeaderboard:")
    if not leaderboard:
        print("No scores yet.")
        return

    sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    for entry in sorted_leaderboard:
        print(f"{entry['name']} - Score: {entry['score']}")

def provide_hint(number_to_guess, guess):
    hints = []
    if number_to_guess % 2 == 0:
        hints.append("Hint: The number is even.")
    else:
        hints.append("Hint: The number is odd.")

    if guess != 0 and number_to_guess % guess == 0:
        hints.append("Hint: The number is divisible by your guess.")
    else:
        hints.append("Hint: The number is NOT divisible by your guess.")

    if is_prime(number_to_guess):
        hints.append("Hint: The number is a prime number.")
    else:
        hints.append("Hint: The number is not a prime number.")

    for hint in hints:
        print(hint)

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def play_round(start, end, max_attempts):
    number = random.randint(start, end)
    attempts = 0

    print(f"\nI'm thinking of a number between {start} and {end}. You have {max_attempts} attempts.")
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts+1}: Enter your guess: "))
            attempts += 1

            if guess == number:
                print(f"Correct! You guessed the number in {attempts} attempts.")
                return max_attempts - attempts + 1  # Score
            elif guess < number:
                print("Too low!")
            else:
                print("Too high!")

            provide_hint(number, guess)
        except ValueError:
            print("Please enter a valid integer.")

    print(f"Sorry, you've used all {max_attempts} attempts. The number was {number}.")
    return 0

def guess_the_number():
    load_leaderboard()
    print_instructions()
    settings = None
    total_score = 0

    while True:
        if not settings:
            settings = settings_menu()
            if settings is None:
                continue

        start, end, attempts = settings
        score = play_round(start, end, attempts)
        total_score += score

        name = input("Enter your name for the leaderboard: ")
        leaderboard.append({'name': name, 'score': score})
        save_leaderboard() 


        again = input("Do you want to play another round? (y/n): ").lower()
        if again != 'y':
            print(f"Thank you for playing! Your total score: {total_score}")
            break

if __name__ == "__main__":
    guess_the_number()
