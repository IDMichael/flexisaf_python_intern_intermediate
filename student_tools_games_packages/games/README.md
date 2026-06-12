Simple Games Package (Mini System)
# Overview

This Python project is a modular Games Package System built using packages and multiple game modules. It allows users to select and play small interactive games from a single main menu.

The system demonstrates real-world software design using:
+ Modular programming (separate files for each game)
+ Function-based structure (each game is independent)
+ Input validation and error handling
+ Exception handling using try, except
+ Random-based game logic using Python’s random module
+ Menu-driven program flow

The program includes three games: Guess Number, Dice Roll, and Rock–Paper–Scissors, all controlled through a central main script.

# Features
* Multiple games in one package system
* Guess Number game (1–10 range with limited attempts)
* Dice Roll simulator (1–6 random values)
* Rock–Paper–Scissors game with scoring system
* Input validation for safe user interaction
* Replay system for continuous gameplay
* Clean modular architecture using Python packages

## Modules Explained
1. Guess Number Game (guess_number.py)
Handles number guessing gameplay logic.

### Responsibilities:
- Generates a random number between 1 and 10
- Allows 3 attempts per game
- Gives hints (Too high / Too low)
- Validates user input safely

### Key Rules:
- Guess must be between 1 and 10
- Input must be a valid number
- Game ends after correct guess or attempts finish

2. Dice Roll Game (dice_roll.py)
Simulates rolling a dice repeatedly.

### Responsibilities:
- Generates random dice values (1–6)
- Allows repeated rolling
- Handles user choice (y/n)

### Key Rules:
- Input must be y or n
- Invalid input ends the game for safety
- Last roll is displayed at the end

3. Rock Paper Scissors Game (rps.py)
Classic user vs computer game system.

### Responsibilities:
- Accepts user move (rock, paper, scissors)
- Generates computer move randomly
- Determines winner using game rules
- Tracks score

### Key Rules:
- Only rock, paper, scissors allowed
- Rock beats scissors
- Scissors beats paper
- Paper beats rock

4. Main Game Controller (games_main.py)
Handles game selection and navigation.

### Responsibilities:
- Displays game menu
- Accepts user choice
- Calls selected game module
- Controls exit system

### Safety Features:
- Prevents empty input
- Ensures numeric menu selection
- Handles invalid options safely

# Technologies Used
Python 3

# Required Libraries
No external libraries are required.
This program uses only Python built-in libraries:

- random
- input()
- try, except
- basic control flow

# How to Run the Program
1. Navigate into the project folder
cd student_tools_games_packages

2. Run the main script
python games_main.py