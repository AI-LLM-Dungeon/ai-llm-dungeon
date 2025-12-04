"""ASCII art assets for the Ground Level of AI-LLM-Dungeon."""

# Welcome banner for Ground Level
GROUND_LEVEL_BANNER = r"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║       ░█▀█░▀█▀░░░█░░░█░░█▀▄░█▀█░█░█░█▀█░█▀▀░█▀▀░█▀█░█▀█   ║
║       ░█▀█░░█░░░░█░░░█░░█░█░█░█░█░█░█░█░█░█░█▀▀░█░█░█░█   ║
║       ░▀░▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀   ║
║                                                            ║
║                   GROUND LEVEL QUEST                       ║
║            Learn the Arts of Ollama Mastery!               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

# Sidekick ASCII Art
PHI3_MINI_ART = r"""
    /\_/\  
   ( o.o ) 
    > ^ <   Phi3 Mini
   /|   |\  
  (_|   |_) 
"""

QWEN_LITE_ART = r"""
    ___
   /   \  
  | O O | 
  |  ^  |  Qwen Lite
   \___/   
   |   |   
  /|   |\  
"""

LLAMA3_8B_ART = r"""
    //\\
   (o  o)
   |  > |   Llama3 8b
   | || |
  /| || |\
 (_|_||_|_)
"""

# Room transition
ROOM_TRANSITION = r"""
    ┌─────────────────────────┐
    │   Moving to next room   │
    └─────────────────────────┘
"""

# Victory/completion screen
VICTORY_SCREEN = r"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ★ ★ ★  CONGRATULATIONS, ADVENTURER!  ★ ★ ★         ║
║                                                       ║
║        You have mastered the Ground Level!            ║
║                                                       ║
║   You've learned the fundamentals of Ollama:          ║
║     • Summoning sidekicks (local LLMs)                ║
║     • Understanding model capabilities                ║
║     • Managing model memory                           ║
║     • Benchmarking with riddles                       ║
║                                                       ║
║        The deeper dungeons await you...               ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
"""

# Tip unlock notification
TIP_UNLOCK_TEMPLATE = r"""
╭───────────────────────────────────╮
│  💡 NEW KNOWLEDGE UNLOCKED! 💡   │
╰───────────────────────────────────╯
  {tip_text}
"""

# Progress indicators
LOADING_DOTS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

def get_sidekick_art(name: str) -> str:
    """Returns ASCII art for a specific sidekick by name."""
    art_map = {
        "Phi3 Mini": PHI3_MINI_ART,
        "Qwen Lite": QWEN_LITE_ART,
        "Llama3 8b": LLAMA3_8B_ART,
    }
    return art_map.get(name, "")

def display_tip_unlock(tip_text: str) -> None:
    """Displays a tip unlock notification."""
    print(TIP_UNLOCK_TEMPLATE.format(tip_text=tip_text))

def display_banner() -> None:
    """Displays the Ground Level welcome banner."""
    print(GROUND_LEVEL_BANNER)

def display_victory() -> None:
    """Displays the victory screen."""
    print(VICTORY_SCREEN)

def display_room_transition() -> None:
    """Displays a room transition animation."""
    print(ROOM_TRANSITION)
