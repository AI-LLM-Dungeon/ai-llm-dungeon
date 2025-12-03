import os
import subprocess
import shlex # For safely splitting shell commands

# Import the tokenizer fight logic
from tokenizer_fight import perform_tokenizer_fight

# --- Game State ---
current_level = 0
level_names = {
    0: "Tokenizer Tomb",
    1: "Temperature Tavern"
}

def display_welcome_banner():
    """Displays the main welcome banner for the AI-LLM-Dungeon."""
    print("========================================")
    print("   WELCOME TO AI-LLM-DUNGEON          ")
    print("========================================\n")

def display_level_intro(level_id):
    """Displays the intro for the current level."""
    if level_id == 0:
        print(f"# {level_names.get(level_id, 'UNKNOWN LEVEL')} (Level {level_id})")
        print("\nYou awaken in darkness. Ancient carvings whisper:")
        print("\"Tokens are the atoms of language models.\"")
        print("\n**Your quest:** Defeat the Subword Goblin by counting tokens.")
        print("\n**Commands:**")
        print("- `tokenizer_fight \"your text here\"` → fight! (Note: 'python' prefix is not needed here!)")
        print("- `ls` → look around")
        print("- `cd ..` → flee (coward)")
        print("\nNext level coming soon: Temperature Tavern")
        print("\nYour first battle begins NOW: try `tokenizer_fight 'Hello, world!'`")
        print("========================================\n")
    else:
        print(f"# {level_names.get(level_id, 'UNKNOWN LEVEL')} (Level {level_id})")
        print("\nMore lore and challenges coming soon for this level!")
        print("========================================\n")

def handle_os_command(command_parts):
    """Handles basic OS commands like 'ls' or 'cd ..'."""
    cmd = command_parts[0]
    args = command_parts[1:]

    if cmd == 'ls':
        try:
            # capture_output=True means it won't print directly, we print it
            result = subprocess.run(['ls'] + args, capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing ls: {e.stderr.strip()}")
        except FileNotFoundError:
            print(f"Error: '{cmd}' command not found.")
    elif cmd == 'cd':
        path = args[0] if args else os.path.expanduser("~") # Default to home for just 'cd'
        try:
            os.chdir(path)
            print(f"Changed directory to: {os.getcwd()}")
            # We don't want to show the current level intro again on 'cd'
        except FileNotFoundError:
            print(f"Error: Directory not found: {path}")
        except PermissionError:
            print(f"Error: Permission denied for {path}")
        except Exception as e:
            print(f"Error changing directory: {e}")
    else:
        print(f"Unknown OS command: {' '.join(command_parts)}")
        print("Available commands within the dungeon are: `tokenizer_fight`, `ls`, `cd ..`")


def game_loop():
    """The main game loop for the AI-LLM-Dungeon CLI."""
    display_welcome_banner()

    while True:
        display_level_intro(current_level)
        prompt = f"[{level_names.get(current_level, 'UNKNOWN LEVEL')}> "
        user_input = input(prompt).strip()

        if not user_input:
            continue # Just press enter, show prompt again

        # Use shlex to correctly parse commands with quotes
        command_parts = shlex.split(user_input)
        
        command = command_parts[0]
        args = command_parts[1:] # Remaining parts are arguments

        if command == "quit" or command == "exit":
            print("Farewell, adventurer! Until next time.")
            break
        elif command == "tokenizer_fight":
            # The user text might be an argument with spaces, so re-join it
            text_to_fight = ' '.join(args)
            perform_tokenizer_fight(text_to_fight)
        elif command == "ls" or command == "cd":
            handle_os_command(command_parts)
            # After OS commands, we don't want to repeat the level intro immediately
            # break and continue help manage loop flow.
            print("\n") # Add a newline for better spacing
            continue # Continue to next iteration, which will display level intro
        else:
            print(f"Unknown dungeon command: '{command}'")
            print("Available commands are: `tokenizer_fight`, `ls`, `cd ..`, `quit`")
            print("\n") # Add a newline for better spacing


if __name__ == "__main__":
    game_loop()
