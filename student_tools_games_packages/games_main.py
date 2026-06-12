from games.guess_number import play as guess_game
from games.dice_roll import play as dice_game
from games.rps import play as rps_game

def main():
	while True:
		print("\n==== SIMPLE GAMES MENU ====")
		print("1. Guess Number")
		print("2. Dice Roll")
		print("3. Rock Paper Scissors")
		print("4. Exit")

		choice = input("Choose option from 1 - 4: ").strip()

		if not choice:
			print("Empty input. Try again.")
			continue

		if not choice.isdigit():
			print("Invalid input. Enter a number between 1 and 4.")
			continue

		choice = int(choice)
		
		if choice == 1:
			guess_game()

		elif choice == 2:
			dice_game()

		elif choice == 3:
			rps_game()

		elif choice == 4:
			print("Goodbye!")
			break

		else:
			print("Invalid option. Choose between 1 and 4.")

if __name__ == "__main__":
	main()