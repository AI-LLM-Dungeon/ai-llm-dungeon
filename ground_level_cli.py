#!/usr/bin/env python3
"""
AI-LLM-Dungeon: Ground Level

A fully playable Python MVP that teaches users about Ollama installation,
model management, sidekick (local LLM) summoning, benchmarking, riddles,
and tip unlocks.

Learn the fundamentals of working with local language models through
an interactive dungeon adventure!
"""

import sys
import os

# Add the parent directory to the path so we can import ground_level
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ground_level.game_engine import GameEngine


def main() -> None:
    """
    Main entry point for the Ground Level CLI game.
    
    Initializes the game engine and starts the main game loop.
    """
    try:
        # Determine the data directory path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "data")
        
        # Check if data directory exists
        if not os.path.exists(data_dir):
            print(f"Error: Data directory not found at {data_dir}")
            print("Please ensure the 'data' directory with JSON files exists.")
            sys.exit(1)
        
        # Initialize and start the game
        game = GameEngine(data_dir=data_dir)
        game.start()
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Error: Required data file not found: {e}")
        print("Please ensure all data files (tips.json, puzzles.json, models.json)")
        print("are present in the 'data' directory.")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n⚠️  Unexpected error: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()
