import random

def play():
    print("\n==== DICE ROLL GAME ====")

    last_roll = None

    while True:
        last_roll = random.randint(1, 6)
        print(f"You rolled: {last_roll}")

        choice = input("Roll again? (y/n): ").strip().lower()

        if choice == "y":
            continue

        elif choice == "n":
            print("Thanks for playing")
            break

        else:
            print("Invalid input. Exiting game for safety.")
            break

    print(f"Final roll: {last_roll}")