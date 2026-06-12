import random

CHOICES = ["rock", "paper", "scissors"]

def get_winner(user, computer):
    if user == computer:
        return "draw"

    if(
        (user == "rock" and computer == "scissors") or
        (user == "paper" and computer == "rock") or
        (user == "scissors" and computer == "paper")
        ):
        return "user"

    return "computer"

def play():
    user_score = 0
    computer_score = 0

    print("\n==== ROCK PAPER SCISSORS ====")

    while True:
        user = input("Choose rock, paper, or scissors: ").strip().lower()

        if user not in CHOICES:
            print("Invalid choice. Try again.")
            continue

        computer = random.choice(CHOICES)
        print(f"Computer chose: {computer}")

        result = get_winner(user, computer)

        if result == "user":
            print("You win!")
            user_score += 1

        elif result == "computer":
            print("Computer wins!")
            computer_score += 1

        else:
            print("It's a draw!")

        print(f"Score - You: {user_score} | Computer: {"computer_score"}")

        again = input("Play again? (y/n): ").strip().lower()

        if again != "y":
            print("Thanks for playing...")
            break