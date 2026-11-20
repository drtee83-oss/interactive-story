import streamlit as st
import random

st.set_page_config(page_title="Escape the Castle!", page_icon="🏰", layout="centered")

# STEP 1 — Initialise game values once per browser session.
# Streamlit reruns the script when the player interacts with a widget.
# These values need to survive those reruns.

if "playerName" not in st.session_state:
    st.session_state.playerName = ""

if "playerHealth" not in st.session_state:
    st.session_state.playerHealth = 100

if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "scene" not in st.session_state:
    st.session_state.scene = "start"

if "result" not in st.session_state:
    st.session_state.result = ""

# STEP 2 — Show the game's title and the information the player carries.

st.title("🏰 Escape the Castle")

if st.session_state.playerName:
    st.write(f"Player: {st.session_state.playerName}")
    st.write(f"Health: {st.session_state.playerHealth}")
    st.write(f"Inventory: {st.session_state.inventory}")

# STEP 3 — Start screen: use a text input and button.
# The name is saved to session state so it is available in later scenes.

if st.session_state.scene == "start":
    st.subheader("Create your character")
    st.session_state.playerName = st.text_input("What is your name?")
    if st.button("Start Adventure"):
        st.session_state.scene = "cell"
        st.rerun()

# STEP 4 — Cell scene: convert the terminal choices into buttons.
# Store the result so it stays visible after other interactions.

elif st.session_state.scene == "cell":
    st.subheader("The Cell")
    st.write("You awake to the sound of water dripping on stone.")
    st.write("You wipe the sleep from your bleary eyes and see blank, grey stone.")
    st.write("As you look around, you see a door, a window, and a bed.")

    if st.button("Investigate the door."):
        st.session_state.result = "The door is locked, you need a key!"
    if st.button("Investigate the window."):
        st.session_state.result = "The window is too small to escape through."
    if st.button("Investigate the bed."):
        if "Iron Key" not in st.session_state.inventory:
            st.session_state.inventory.append("Iron Key")
            st.session_state.result = "You found an Iron Key!"
        else:
            st.session_state.result = "There is nothing else under the bed."
    if st.session_state.result:
        st.info(st.session_state.result)

# STEP 5 — Unlock progress using a condition based on inventory.

    if "Iron Key" in st.session_state.inventory:
        if st.button("Unlock the door and continue?"):
            st.session_state.scene = "corridor"
            st.session_state.result = ""
            st.rerun()

# STEP 6 — Corridor scene: use the SAME inventory as in the Cell.
 
# Initialise the corridor scene - they player needs to notice a cabinet
 
# Give the player options to "Open the cabinet" or "Leave the cabinet"
 
# If the player opens the cabinet, they should find a rusty dagger

# Allow the player to continue with or without the dagger

elif st.session_state.scene == "corridor":
    st.subheader("The Corridor")
    st.write("You exit the cell and find yourself in a dimly lit corridor.")
    st.write("As you walk along the corridor, you notice an old wooden cabinet.")

    if st.button("Open the cabinet."):
        if "Rusty Dagger" not in st.session_state.inventory:
            st.session_state.inventory.append("Rusty Dagger")
            st.session_state.result = "You find a Rusty Dagger!"
        else:
            st.session_state.result = "The cupboard is bare..."
    if st.button("Leave the cabinet alone."):
        if "Rusty Dagger" in st.session_state.inventory:
            st.session_state.result = "You have already taken the cabinet's contents."
        else:
            st.session_state.result = "You decide to leave the cabinet unopened."
    if st.session_state.result:
        st.info(st.session_state.result)

    if st.session_state.result:
        if st.button("Continue along the corridor?"):
            st.session_state.scene = "crypt"
            st.session_state.result = ""
            st.rerun()

    