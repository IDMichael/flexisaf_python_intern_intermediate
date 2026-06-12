import random

def play():
	target = random.randint(1, 10)
	attempts = 3

	print("\n==== GUESS NUMBER GAME ====")
	print("Guess a number form 1 - 10")
	print(f"You have {attempts} attempts.\n")

	while attempts > 0:
		guess = input("Enter your guess: ").strip()

		if not guess:
			print("Empty input. Try again.")
			continue

		try:
			guess = int(guess)
		except ValueError:
			print("Invalid input. Please enter a valid number.")
			continue

		if guess < 1 or guess > 10:
			print("Guess must be between 1 and 10.")
			continue

		if guess == target:
			print("Correct! You guessed right!")
			return

		elif guess < target:
			print("Too low. Try a higher number.")

		else:
			print("Too high. Try a lower number.")

		attempts -= 1
		print(f"Attempts left: {attempts}")

	print(f"Game over. The correct number was {target}!!!")


