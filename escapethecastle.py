#Welcome the player
print("===ESCAPE THE CASTLE===")
print("Welcome, adventurer!")

#Get player name, age and character class
playerName = input("What is your name? ")
playerAge = int(input("How old are you? "))
playerClass = input("Choose a character class: ")
 
#Set starting values
health = 100
gold = 20
hasKey = False

#Display the character profile
print("\n===YOUR CHARACTER===")
print(f"Name: {playerName}")
print(f"Age: {playerAge}")
print(f"Class: {playerClass}")
print(f"Health: {health}")
print(f"Gold: {gold}")
print(f"Has Key: {hasKey}")

#Begin the story
print(f"\n{playerName}, you wake up in a dark castle.")
print("You hear footsteps approaching...")
print("Your adventure is about to begin!")