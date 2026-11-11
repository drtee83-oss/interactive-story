#Welcome the player
print("===ESCAPE THE CASTLE!===")
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

# ==========================================
# ESCAPE THE CASTLE - SCENE 1: THE CELL
# ==========================================
 
# Introduce the scene to the player
print("Your wake up in dark castle cell.")
print("You can see a door, a window, and an old bed.")

# Ask the player what they want to investigate
# .lower() converts their answer to lowercase
choice = input("Do you want to investigate the door, window, or bed?: ").lower()

# Check whether the player chose the door
if choice == "door":
    print("You walk towards the door.")
    print("You try the handle, but it's locked.")

# Check whether the player chose the window
elif choice == "window":
    print("You look through the window.")
    print("It's too small to escape through.")

# Check whether the player chose the bed
elif choice == "bed":
    print("You look under the bed.")
    print("You find a small, iron key!")

# If none of the options was chosen
else:
    print("You decide not to investigate.")