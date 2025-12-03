import sys
import tiktoken

def get_tokenizer(model_name="cl100k_base"):
    """
    Returns an encoding for a given model.
    For OpenAI models, common encodings are:
    - 'cl100k_base' (for gpt-4, gpt-3.5-turbo, text-embedding-ada-002)
    - 'p50k_base' (for CodeX models, text-davinci-002, text-davinci-003)
    - 'r50k_base' (for gpt2, text-davinci-001)
    """
    try:
        encoding = tiktoken.get_encoding(model_name)
    except ValueError:
        print(f"Error: Unknown tokenizer model '{model_name}'. Falling back to 'cl100k_base'.")
        encoding = tiktoken.get_encoding("cl100k_base")
    return encoding

def count_tokens(text: str, encoding) -> int:
    """Counts tokens in a given text using the provided encoding."""
    tokens = encoding.encode(text)
    return len(tokens)

def display_game_intro():
    """Prints the intro and instructions for Tokenizer Tomb."""
    print("========================================")
    print("   WELCOME TO AI-LLM-DUNGEON          ")
    print("========================================")
    print("# TOKENIZER TOMB (Level 0)             ")
    print("\nYou awaken in darkness. Ancient carvings whisper:")
    print("\"Tokens are the atoms of language models.\"")
    print("\n**Your quest:** Defeat the Subword Goblin by counting tokens.")
    print("\n**Commands:**")
    print("- `python tokenizer_fight.py \"your text here\"` → fight!")
    print("- Win by keeping under 10 tokens")
    print("- `ls` → look around")
    print("- `cd ..` → flee (coward)")
    print("\nNext level coming soon: Temperature Tavern")
    print("\nYour first battle begins NOW:")
    print("python tokenizer_fight.py 'Hello, world!'")
    print("========================================")

def main():
    if len(sys.argv) < 2:
        display_game_intro()
        # If no arguments, we just show the intro. The player needs to provide text.
        return

    user_text = sys.argv[1]
    
    # Initialize tokenizer (using cl100k_base as it's common for modern OpenAI models)
    tokenizer = get_tokenizer("cl100k_base")

    token_count = count_tokens(user_text, tokenizer)

    print("\n--- TOKENIZER FIGHT RESULTS ---")
    print(f"Your input: '{user_text}'")
    print(f"Token count: {token_count} tokens")

    winning_limit = 10

    if token_count < winning_limit:
        print(f"\n✨ VICTORY! ✨")
        print(f"You kept your message brief enough (under {winning_limit} tokens)!")
        print("The Subword Goblin whimpers and retreats into the shadows.")
        print("You feel a surge of understanding about token efficiency.")
    else:
        print(f"\n☠️ DEFEAT! ☠️")
        print(f"Alas, your message was too verbose! ({token_count} tokens >= {winning_limit})")
        print("The Subword Goblin cackles, savoring each extra token.")
        print("Perhaps try a more concise phrasing next time?")

    print("-------------------------------")

if __name__ == "__main__":
    main()
