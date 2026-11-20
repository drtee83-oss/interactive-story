import os
import streamlit as st
import random
from dotenv import load_dotenv
from google import genai
 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
 
client = genai.Client(api_key=api_key) if api_key else None
 
MODEL_NAME = "gemini-3.5-flash-lite"

# ================================================================
# 1. PAGE SETUP — SAME APPROACH AS THE FINAL APP
# ================================================================
# page_icon uses the Unicode castle character, not an image file.
# Keep this before other Streamlit display calls.
st.set_page_config(page_title="Escape the Castle!", page_icon="🏰", layout="centered")
st.title("🏰 Escape the Castle!")

# ================================================================
# 2. GAME SETUP — INITIALISE VALUES ONCE & STRUCTURED PROMPT
# ================================================================
# Session state remembers values when Streamlit reruns the script.
if "game_started" not in st.session_state:
    st.session_state.game_started = False
 
def start_game(name):
    """Set the same starting values and seven-room route as the final app."""
    st.session_state.game_started = True
    st.session_state.player_name = name
    st.session_state.health = 5
    st.session_state.max_health = 5
    st.session_state.inventory = ["Torch"]
    st.session_state.rooms = ["cell", "corridor", "crypt", "library",
        "guard_room", "dungeon", "castle_gate"]
    st.session_state.room_number = 0
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False

def restart_game():
    st.session_state.clear()
    st.rerun()
 
def get_current_room():
    """Use the room number to find the name of the current room."""
    return st.session_state.rooms[st.session_state.room_number]
 
def continue_game():
    """Clear the last action and move to the next room."""
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False
    st.session_state.room_number += 1
    st.rerun()

def add_item(item):
    if item not in st.session_state.inventory:
        st.session_state.inventory.append(item)

def has_item(item):
    return item in st.session_state.inventory

def remove_item(item):
    if item in st.session_state.inventory:
        st.session_state.inventory.remove(item)

def take_damage(amount):
    st.session_state.health -= amount
    if st.session_state.health < 0:
        st.session_state.health = 0

def heal_player(amount):
    old_health = st.session_state.health
    st.session_state.health = min(st.session_state.max_health, st.session_state.health + amount)
    return st.session_state.health - old_health

def generate_story(room, action, outcome, fallback_message):
    if client == None:
        return fallback_message


    inventory_text = ", ".join(st.session_state.inventory)

    prompt = f"""
You are the storyteller for a dark fantasy
adventure game called Escape the Castle.
 
Player: {st.session_state.player_name}
Room: {room}
Health: {st.session_state.health}/{st.session_state.max_health}
Inventory: {inventory_text}
 
Action:
{action}
 
Outcome:
{outcome}
 
Describe what happens in 30-50 words.
 
Use second person.
Use atmospheric dark fantasy language.
Do not change the outcome.
Do not change health or inventory.
Do not introduce new choices.
"""
    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
            generation_config={"thinking_level": "minimal"}
        )
        if interaction.output_text:
            return interaction.output_text
        return fallback_message
    except Exception as error:
        st.error(f"Gemini error: {error}")
        return fallback_message

def roll_dice():
    return random.randint(1,6)

def chance_encounter(button_text, room, action, success_number, success_outcome, success_fallback, failure_outcome, failure_fallback, damage, bonus_item ="", success_item=""):
    if st.button(button_text):
        roll = roll_dice()
        if bonus_item != "" and has_item(bonus_item):
            roll = roll + 2
        if roll >= success_number:
            story = generate_story(room, action, success_outcome, success_fallback)
            set_result("success", story)
        else:
            take_damage(damage)
            story = generate_story(room, action, failure_outcome, failure_fallback)
            set_result("damage", story, damage)
        st.rerun

# ================================================================
# 3. REUSABLE DISPLAY FUNCTIONS — KEEP EVERY ROOM CONSISTENT
# ================================================================
def show_room(title, description):
    """Display a room heading and its description."""
    st.header(title)
    st.write(description)
 
def show_player_info():
    st.subheader(f"🧑 {st.session_state.player_name} ")
    left, right = st.columns(2)
    with left:
        st.write(f"❤️ Health: {st.session_state.health} / {st.session_state.max_health}")
    with right:
        st.write(f"🎒 Inventory: {', '.join(st.session_state.inventory)}")  
    st.caption(
        f"Room {st.session_state.room_number + 1} "
        f"of {len(st.session_state.rooms)}"
    )
    st.divider()

def set_result(result_type, message, value=""):
    st.session_state.result_type = result_type
    st.session_state.result_message = message
    st.session_state.result_value = value
    st.session_state.action_complete = True
    st.rerun()
 
def show_result():
    kind = st.session_state.result_type
    value = st.session_state.result_value
 
    if kind == "item":
        st.success(f"🎒 NEW ITEM: {value}")
    elif kind == "damage":
        st.error(f"💔 DAMAGE: You lose {value} health.")
    elif kind == "heal":
        st.success(f"💚 HEALED: You recover {value} health.")
    elif kind == "success":
        st.success("✅ Success!")
    else:
        st.info("The journey continues...")
 
    st.write(st.session_state.result_message)
 
def show_continue_button(text = "Continue"):
    if st.button(text):
        continue_game()

# ================================================================
# 4. START SCREEN — NAME INPUT FROM DAY 1
# ================================================================
if not st.session_state.game_started:
    st.write("You wake beneath an ancient castle. Your goal is to escape.")
    name = st.text_input("What is your name?")
 
    if st.button("Enter the Castle"):
        if name.strip():
            start_game(name)
            st.rerun()
        else:
            st.warning("Enter your name first before starting ")
else:
    # Show the same player information on every room.
    show_player_info()
    room = get_current_room()

    if st.session_state.health <= 0:
        show_room("💀 Game Over", "Your strength gives out. The castle has claimed another victim.")
        st.error("You did not escape the castle")
        if st.button("🔄 Try Again"):
            restart_game()
        st.stop()

    # ============================================================
    # ROOM 1 — CELL (MODEL SIMPLE CONTINUE NAVIGATION)
    # ============================================================
    if room == "cell":
        show_room("🔒 The Cell", "You wake up inside a cold, dark cell.")
        show_continue_button("🚪 Leave the cell")

    # ============================================================
    # ROOM 2 — CORRIDOR (MODEL RESULT -> CONTINUE)
    # ============================================================
    elif room == "corridor":
        show_room("🕯️ The Corridor", "A wooden cabinet stands beside the staircase.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Investigate"):
                    add_item("Rusty Dagger")
                    story = generate_story(
                        "Corridor", 
                        "the player opens the cabinet and finds a rusty dagger", 
                        "You open the cabinet and find a Rusty Dagger!", 
                        "You open the cabinet and find a Rusty Dagger!"
                        )
                    set_result("item", story, "Rusty Dagger")
            with right:
                if st.button("➡️ Ignore"):
                    story = generate_story(
                        "Corridor", 
                        "the player decides not to open the cabinet", 
                        "You decide not to open the cabinet.", 
                        "You decide not to open the cabinet."
                        )
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()
    # ============================================================
    # ROOM 3 — CRYPT
    # ============================================================
    elif room == "crypt":
        show_room(" ⚰️ The Crypt", "You enter a cold, dim room with a stone coffin. You see a metal glint on the floor beside it.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                roll = roll_dice()
                if roll >= 4:
                    add_item("Iron Key")
                    story = generate_story(
                    "The Crypt",
                    "You investigate the metal glint",
                    "You bend to examine the metal glint and find a small Iron Key!",
                    "You bend to examine the metal glint and find a small Iron Key!"
                    )
                    set_result("item", story, "Iron Key")
                else:
                    take_damage(1)
                    story = generate_story(
                    "The Crypt",
                    "You investigate the metal glint",
                    "You are bitten by a spider hidden among the detritus on the floor!",
                    "You are bitten by a spider hidden among the detritus on the floor!"
                    )
                    set_result("damage", story, 1)
            with right:
                if st.button("➡️ Ignore"):
                    story = generate_story(
                    "The Crypt", 
                    "the player disregards the glinting metal in favour of pressing onwards", 
                    "The player ignores the metal glint and moves on up a wooden staircase in the opposite wall", 
                    "You disregard the metal glint and walk up a wooden staircase set into the opposite wall."
                    )
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()
    #show_room("⚰️ The Crypt", "A metal object glints beside a stone coffin.")
    #Player should be given the choice to investigate the coffin or leave
    #If they do investigate they should obtain an Iron Key
 
 
    # ============================================================
    # ROOM 4 — LIBRARY
    # ============================================================
    elif room == "library":
        show_room(" 📗 The Library", "You enter a warmly lit room filled with floor-to-ceiling bookshelves. A green shimmer coming from one of the books catches your eye.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Investigate"):
                    add_item("Unlocking Spell")
                    outcome = "You open the book and see a spell: alohomora"
                    story = generate_story(
                        "Library", "the player opens a shimmering green book and finds an unlocking spell called 'alohomora'", outcome, "You open the book and see a single, glowing green word: alohomora."
                        )
                    set_result("item", story, "Unlocking Spell")
            with right:
                if st.button("➡️ Ignore"):
                    outcome = "You ignore the shimmering green book and press onwards"
                    story = generate_story(
                        "Library", "the player ignores the shimmering green book in favour of pressing onwards", outcome, "You ignore the shimmer. Who needs a glowing book anyway?"
                        )
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()
    #show_room("📚 The Forgotten Library", "A strange green light shines from an old book.")
    # Give the player the option to investigate or leave

    # ============================================================
    # ROOM 5 — GUARD ROOM
    # ============================================================
    elif room == "guard_room":
        show_room("⚔️ The Guard Room", "A ghostly knight blocks the doorway.")
        if "Rusty Dagger" in st.session_state.inventory:
            st.info("⚔️ You are carrying a Rusty Dagger.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("⚔️ Fight"):
                    outcome = "You defeat the knight and can continue."
                    story = generate_story(
                        "The Guard Room", "the player decides to fight the ghostly knight", outcome, "You dodge the knight's sword. The armour crashes to the floor."
                    )
                    set_result("success", story)
            with right:
                if st.button("🏃 Run"):
                    outcome = "You escape past the knight without injury."
                    story = generate_story(
                        "The Guard Room", "the player decides to flee the encounter", outcome, "You sprint past the knight and escape through the doorway."
                    )
                    set_result("success", story)
        else:
            show_result()
            show_continue_button()

    # ============================================================
    # ROOM 6 — DUNGEON (INVENTORY PERSISTS ACROSS ROOMS)
    # ============================================================
    elif room == "dungeon":
        show_room("🕸️ Dungeon", "You enter a dank dungeon. A shelf full of dusty bottles lies directly ahead.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Investigate"):
                    outcome = "You find a healing potion among the bottles"
                    story = generate_story("Dungeon", "finding a healing potion", outcome, "You pilfer a bottle of red liquid labelled 'HEAL'.")
                    add_item("Healing Potion")
                    set_result("item", story, "Healing Potion")
            with right:
                if st.button("➡️ Ignore"):
                    outcome = "You ignore the bottles and continue on"
                    story = generate_story("Dungeon", "ignoring the shelf of dusty bottles and moving on", outcome, "Nothing on the shelf appeals to you. You walk away without taking anything.")
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()
 
    #see a bottle of red liquid
    #left - take it, find a healing potion
    #right - leave it, leave the bottle behind
 
    # ============================================================
    # ROOM 7 — CASTLE GATE (BRANCH BASED ON INVENTORY)
    # ============================================================
    elif room == "castle_gate":
        escaped = False
        show_room("🧱 The Castle Gate", "A large iron gate blocks your path, set into the ivy-covered rampart wall.")
        if "Iron Key"  in st.session_state.inventory:
            st.info("🗝️ You are carrying an Iron Key.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            if "Iron Key" in st.session_state.inventory:
                with left:
                    if st.button("🗝️ Try the Iron Key"):
                        outcome = "You use the key to unlock the padlock and escape"
                        story = generate_story("The Castle Gate", "using the key to unlock the padlock and escape", outcome, "You use the key to unlock the padlock and escape.")
                        set_result("success", story)
                with right:
                    if st.button("🔒 Check the padlock"):
                        outcome = "You jiggle the padlock. It doesn't budge."
                        story = generate_story("The Castle Gate", "you jiggle the padlock but it doesn't yield", outcome, "The padlock is unyielding. Maybe the Iron Key will be useful?")
                        st.info(story)
            else:
                with left:
                    if st.button("🧗 Climb the wall"):
                        outcome = "You use the ivy to climb the wall and escape"
                        story = generate_story("The Castle Gate", "using the ivy to unlock the climb the wall and escape", outcome, "You use the ivy to climb the wall and escape.")
                        set_result("success", story)
                with right:
                    if st.button("🔒 Check the padlock"):
                        st.info("The padlock is unyielding. Maybe you can climb the wall?")
        else:
            show_result()
            st.header("🏆 YOU ESCAPED THE CASTLE!")
            st.balloons()

            st.divider()
            if st.button("🔁 Play Again?"):
                restart_game()
 
    #use the guard room as the template
    #check to see if Iron Key held in inventory
    #if key in inventory, show button to unlock the gate and escape
    #if no key in inventiory show button to climb the wall and escape