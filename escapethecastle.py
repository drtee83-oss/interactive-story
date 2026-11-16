# ==========================================
# ESCAPE THE CASTLE - COMPLETE GAME
# ==========================================
 
import random
 
# Define shared inventory
inventory = []
 
 
# ==========================================
# INTRODUCTION - COPY DAY 2 CODE
# ==========================================

# Intro function
def introduction():
    
    # Welcome the player
    print("\n===ESCAPE THE CASTLE!===")
    print("Welcome, adventurer!")

    # Get player name, age and character class
    playerName = input("What is your name? ")
    playerAge = int(input("How old are you? "))
    playerClass = input("Choose a character class: ")
    
    # Set starting values
    health = 100
    gold = 20

    # Display character profile
    print("\n===YOUR CHARACTER===")
    print(f"Name: {playerName}")
    print(f"Age: {playerAge}")
    print(f"Class: {playerClass}")
    print(f"Health: {health}")
    print(f"Gold: {gold}")

    # Story intro
    print(f"\nWelcome, {playerName}!")
    print("You awake to the sound of water dripping on stone.")
    print("You wipe the sleep from your bleary eyes and see blank, grey stone.")
 
    # TODO:
    # Copy your character creation code here.
    #
    # Include:
    # - Welcome message
    # - Player name
    # - Character class
    # - Starting health and gold
    #
    # Remember to indent your code!
 
 
# ==========================================
# CELL - COPY DAY 3/4 CODE
# ==========================================

# Cell scene
def cell():

    # Key variable
    hasKey = False

    # Scene intro
    print("\nAs you shake the cobwebs from your mind and sit up, you see that you are in dark, dank cell.")
    print("You can see a door, a window, and an old bed.")

    # Key loop
    while hasKey == False:

        # Ask the player what they want to investigate
        choice = input("\nDo you want to investigate the [door], [window], or [bed]?:\n>>> ").lower()

        # Check whether the player chose the door
        if choice == "door":
            print("You walk towards the door.")
            print("You try the handle, but it's locked. Could there be a key somewhere?")

        # Check whether the player chose the window
        elif choice == "window":
            print("You look through the window.")
            print("It's too small to escape through.")

        # Check whether the player chose the bed
        elif choice == "bed":
            print("You look under the bed.")
            print("You find a small, Iron Key!")
            hasKey = True
            inventory.append("Iron Key")

        # If none of the options was chosen
        else:
            print("That is not a valid option. Please choose [door], [window], or [bed].\n>>> ")

    # Scene conclusion
    print("\nYou unlock the cell door.")
    print("You step out into the corridor.")
    print(f"   Your inventory now contains: {inventory}")
 
    # TODO:
    # Copy your Cell scene here.
    #
    # Include:
    # - Door, window and bed choices
    # - While loop
    # - Finding the Iron Key
    # - Adding the key to inventory
    #
    # Remove any separate inventory = []
    # from your original scene.
 
 
# ==========================================
# RANDOM ENCOUNTER - COPY DAY 4 CODE
# ==========================================

# Encounter function
def encounter(creature):

    # Creature responses 
    print(f"\nA {creature} appears!!")
    if creature == "Guard":
        print("The guard draws their sword!")
    elif creature == "Ghost":
        print("The ghost emits an ethereal wail...")
    elif creature == "Rat":
        print("The rat squeaks inquisitively.")

    # Scene conclusion
    print("\nYou flee!")

    # TODO:
    # Copy your encounter function here.
    #
    # Include:
    # - Guard
    # - Ghost
    # - Rat
    # - Different messages for each creature
 
 
# ==========================================
# CORRIDOR - COPY DAY 3/4 CODE
# ==========================================

# Corridor scene
def corridor():

    # Scene intro
    print("\nYou enter a long, dark corridor.")
    print("You notice an old wooden cabinet.")

    # Ask the player if they want to open the cabinet
    choice = input("Do you open the cabinet?:\n>>> ").lower()

    # Positive response
    if choice == "yes":
        print("You open the cabinet.")
        print("Inside, you find a Rusty Dagger!")
        inventory.append("Rusty Dagger")

    # Negative response
    elif choice == "no":
        print("You leave the cabinet closed.")

    # Inventory check
    print(f"   Your inventory contains: {inventory}")

    # List possible creatures
    creatures = ["Guard", "Ghost", "Rat"]

    # Pick a random creature
    randomCreature = random.choice(creatures)

    # Run encounter
    encounter(randomCreature)

    # TODO:
    # Copy your Corridor scene here.
    #
    # Include:
    # - Cabinet choice
    # - Finding the Rusty Dagger
    # - Adding the dagger to inventory
    #
    # Then add:
    # - List of possible creatures
    # - random.choice()
    # - Call encounter() with the chosen creature
 
 
# ==========================================
# LIBRARY - NEW SCENE
# ==========================================
 
# Library scene
def library():

    # Clue variable
    hasClue = False

    # Introduce the scene
    print("\nYou enter the door at the end of the corridor and find a library.")
    print("There is a smell of musty old books as you browse the shelves.")

    while hasClue == False:
        # Ask the player what they want to investigate
        choice = input("There are several books on the shelf in front of you.\n Would you like to look at the large, [red] book; the small, [blue] book, or the thick, [green] book?\n>>> ").lower()

        # If the player chose red
        if choice == "red":
            print("You pick up the large, red book and idly leaf through the pages.")
            print("There is nothing of interest, just spellcraft diagrams.")

        # If the player chose blue
        elif choice == "blue":
            print("You pick up the small, blue book.")
            print("It looks to be the journal of an ancient warlord. Nothing stands out.")

        # If the player chose green
        elif choice == "green":
            print("You pick up the thick, green book. It's so heavy you almost drop it.")
            print("The book falls open, spraying dust in your face. As the dust clears, you notice a small scrap of paper with the word 'anvil' written on it.")
            hasClue = True
            inventory.append("Password Clue")

        # If none of the options was chosen
        else:
            print("That is not a valid option. Please choose [red], [blue], or [green].")

    # Scene conclusion
    print("You hastily shove the scrap of paper into your pocket and exit through the opposite door.")

    # Inventory check
    print(f"   Your inventory now contains: {inventory}")

 
    # TODO:
    # Create a Library scene.
    #
    # The player discovers a clue to the
    # password needed to escape the castle.
    #
    # Use:
    # - print()
    # - input()
    # - if/elif/else
    # - A while loop
 
 
# ==========================================
# CASTLE GATE - NEW SCENE
# ==========================================

# Castle gate scene
def castle_gate():
    correctPassword = False

    # Scene intro
    print("\nThe door exits into the entrance hall of the castle. You can see the main doors standing ajar. The hall is deserted.")
    print("You dash through the doors into the courtyard. Ahead is a gate with a portcullis, a guard stood either side.")
    print("The guard on the left holds out his hand commandingly, right hand clutching his lance in readiness. 'PASSWORD', he barks.")

    # Password variable
    while correctPassword == False:

        # Ask the player to enter the password
        choice = input("You stammer out the password nervously:\n>>> ")

        # If the player gets the password correct
        if choice == "anvil":
            print("The guard looks suspicious but grunts and allows you to pass.")
            correctPassword = True

        # If the player enters a similar password
        elif choice == "hammer":
            print("The guard eyes you, lifting his lance a few inches off the ground. 'Close... are you sure you're not just guessing?', he asks.")

        # If the player gets the password wrong
        else:
            print("'Wrong! You shall not pass!', the guard roars, taking a menacing step towards you.")
            print("You flee, back into the relative safety of the castle entrance hall.")

    # Scene and game conclusion
    print("\nThe guard raises the portcullis and allows you to exit the courtyard.")
    print("You suppress a sigh of relief and walk through the gate.")
    print("Congratulations, you have escaped!")


 
    # TODO:
    # Create the final escape challenge.
    #
    # The player must enter the correct
    # password to unlock the gate.
    #
    # Use a while loop to allow retries.
    #
    # Display a victory message when
    # the player escapes.
 
 
# ==========================================
# MAIN GAME
# ==========================================

# Game sequence
def play_game():
 
    introduction()
    cell()
    corridor()
    library()
    castle_gate()
 
 
# Start the game
play_game()