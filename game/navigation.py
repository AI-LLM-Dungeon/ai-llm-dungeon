"""Shared navigation system for transitioning between dungeon levels."""

import os
import glob


def show_descend_menu(current_level_name: str = "Ground Level") -> None:
    """
    Display the descend menu with available levels and navigation instructions.
    
    This function is called when a player completes a level and is ready
    to descend deeper into the dungeon. It dynamically discovers all available
    level CLI files and provides clear instructions for continuing the adventure.
    
    Args:
        current_level_name: Name of the level just completed (e.g., "Ground Level", "Token Crypts")
    """
    print("\n" + "="*60)
    print("🎉 CONGRATULATIONS! 🎉")
    print("="*60)
    print(f"\nYou have completed {current_level_name}!")
    print("The path descends deeper into the AI-LLM-Dungeon...")
    print()
    
    # Discover available level CLI files
    cli_files = sorted(glob.glob("*_cli.py"))
    
    if cli_files:
        print("📚 AVAILABLE LEVELS:")
        print()
        for cli_file in cli_files:
            # Extract level name from filename (e.g., "ground_level_cli.py" -> "Ground Level")
            level_name = cli_file.replace("_cli.py", "").replace("_", " ").title()
            print(f"   • {level_name}: python3 ./{cli_file}")
        print()
    
    print("🔍 DISCOVER NEW LEVELS:")
    print("   List all playable scripts: ls *_cli.py")
    print("   (Playable scripts always have the '_cli' suffix)")
    print()
    
    print("🔄 GET UPDATES:")
    print("   Check for new levels and features: git pull origin main")
    print()
    
    print("🔗 RESOURCES:")
    print("   • GitHub: https://github.com/AI-LLM-Dungeon/ai-llm-dungeon")
    print("   • Report Issues: https://github.com/AI-LLM-Dungeon/ai-llm-dungeon/issues")
    print("   • ⭐ Star the repo to follow updates!")
    print()
    
    print("="*60)
    print("Choose your path:")
    print("   • Type 'west' to revisit completed rooms")
    print("   • Type 'quit' to exit and play another level")
    print("="*60)
    print()
