"""Room class for the Ground Level of AI-LLM-Dungeon."""

from typing import Optional, Callable, List
from .sidekick import Sidekick
from .puzzle import Puzzle
from .player import Player


class Room:
    """
    Represents a room in the Ground Level dungeon.
    
    Each room has a description, optional sidekick, optional puzzle, and
    specific objectives that must be completed before the player can proceed.
    
    Attributes:
        room_id (int): Unique identifier for the room
        name (str): Name of the room
        description (str): Detailed description of the room
        objectives (List[str]): List of objectives to complete in this room
        completed (bool): Whether all objectives are completed
        available_directions (List[str]): Directions the player can move
    """
    
    def __init__(
        self,
        room_id: int,
        name: str,
        description: str,
        objectives: Optional[List[str]] = None
    ):
        """
        Initialize a new Room.
        
        Args:
            room_id: Unique identifier for the room
            name: Name of the room
            description: Detailed description of the room
            objectives: List of objectives to complete (optional)
        """
        self.room_id: int = room_id
        self.name: str = name
        self.description: str = description
        self.objectives: List[str] = objectives or []
        self.completed: bool = False
        self.available_directions: List[str] = []
        self.first_visit: bool = True
    
    def enter(self, player: Player) -> None:
        """
        Called when the player enters this room.
        
        Displays the room description and available actions.
        
        Args:
            player: The player entering the room
        """
        print(f"\n{'='*60}")
        print(f"  {self.name} (Room {self.room_id})")
        print(f"{'='*60}\n")
        
        if self.first_visit:
            print(self.description)
            self.first_visit = False
        else:
            print("You've returned to this room.")
        
        print()
        self._show_objectives()
        print()
    
    def _show_objectives(self) -> None:
        """Display the current objectives for this room."""
        if not self.objectives:
            return
        
        print("📋 OBJECTIVES:")
        for i, objective in enumerate(self.objectives, 1):
            print(f"  {i}. {objective}")
    
    def mark_completed(self) -> None:
        """Mark this room as completed."""
        self.completed = True
    
    def show_available_actions(self) -> None:
        """Display available actions in this room."""
        print("\n⚔️  AVAILABLE ACTIONS:")
        print("  'status'  - View your current status")
        print("  'tips'    - View unlocked knowledge tips")
        print("  'help'    - Show available commands")
        print("  'quit'    - Exit the game")
    
    def __str__(self) -> str:
        """String representation of the room."""
        status = "✓" if self.completed else "○"
        return f"{status} Room {self.room_id}: {self.name}"


class OllamaVillage(Room):
    """
    Room 0: Ollama Village
    
    The starting area where the Shaman teaches the player real Ollama commands
    before they enter the dungeon proper.
    """
    
    def __init__(self):
        description = """
You find yourself in a peaceful village nestled at the base of a great mountain.
The air hums with ancient knowledge. 

Before you stands a wise Shaman, keeper of the Ollama arts.
The Shaman speaks: "Welcome, young apprentice! Before you venture into the 
dungeon depths, you must first learn the sacred commands of Ollama."

"I will teach you the essential commands that every Ollama master must know.
Listen carefully, for these commands will be your tools in the challenges ahead."

💡 Hint: Type 'learn' to begin your training with the Shaman!
        """
        
        objectives = [
            "Learn about installing Ollama",
            "Learn the 'ollama serve' command",
            "Learn the 'ollama list' command",
            "Learn the 'ollama pull' command",
            "Learn the 'ollama run' command",
            "Learn the 'ollama show' command",
            "Learn the 'ollama rm' command"
        ]
        
        super().__init__(0, "Ollama Village", description.strip(), objectives)
        self.available_directions = ["east"]  # Can go to Room 1 after training
        self.lessons_completed = 0
        self.total_lessons = 7


class SummoningChamber(Room):
    """
    Room 1: The Summoning Chamber
    
    Teaches the player how to summon their first sidekick (Phi3 Mini)
    using the exact scroll text.
    """
    
    def __init__(self):
        description = """
You enter the mystical Summoning Chamber, the first true test of your training.
Glowing runes on the walls read:

  "To master the LLMs, one must summon them with the proper incantations."
  "Use the Ollama command you learned in the village."

On a pedestal before you lies an instruction scroll for "Phi3 Mini":
  Model: phi3:mini
  Command: ollama pull phi3:mini

To summon your first sidekick, use the command shown above.
        """
        
        objectives = [
            "Read the instruction scroll on the pedestal",
            "Summon Phi3 Mini using: ollama pull phi3:mini"
        ]
        
        super().__init__(1, "The Summoning Chamber", description.strip(), objectives)
        self.available_directions = ["west", "east"]  # Can go back to village or forward


class RiddleHall(Room):
    """
    Room 2: The Riddle Hall
    
    Presents the strawberry riddle. Phi3 Mini attempts but fails,
    demonstrating small model limitations.
    """
    
    def __init__(self):
        description = """
You enter a grand hall with crystalline walls that shimmer with data streams.
At the center stands a mysterious Oracle of Puzzles, and behind her, you notice
a magnificent treasure chest sealed with ancient locks.

The Oracle speaks: "Many adventurers have attempted my riddles.
Some succeed, some fail. Your companion's strength will be tested here.
Answer correctly, and the treasure chest shall open, revealing the password
to the Victory Chamber."

A riddle materializes in glowing text before you:
  "How many 'r's are in 'strawberry'?"

To consult your sidekick, use: ollama run phi3:mini
        """
        
        objectives = [
            "Use 'ollama run phi3:mini' to consult your sidekick",
            "Ask about the strawberry riddle",
            "Use a stronger, more capable model to complete the riddle"
        ]
        
        super().__init__(2, "The Riddle Hall", description.strip(), objectives)
        self.available_directions = ["west", "east"]  # Can go back or forward


class UpgradeForge(Room):
    """
    Room 3: The Upgrade Forge
    
    Teaches model management: removing Phi3 Mini and summoning Llama3 8b.
    """
    
    def __init__(self):
        description = """
You discover an ancient forge where models are crafted and refined.
A wise forge master appears and speaks:

"I see your small companion has reached their limits. Fear not!
The forge can reshape your tools. You must first release Phi3 Mini
to make room for a more powerful ally."

On the wall, you see Ollama commands carved in stone:
  1. Inspect your current model: ollama show phi3:mini
  2. Remove your current model: ollama rm phi3:mini
  3. Pull a more powerful model: ollama pull llama3:8b
  4. Return WEST to retry the riddle with greater strength

The forge master awaits your command.
        """
        
        objectives = [
            "Remove Phi3 Mini: ollama rm phi3:mini",
            "Pull and summon Llama3 8b: ollama pull llama3:8b",
            "Return west to retry the riddle"
        ]
        
        super().__init__(3, "The Upgrade Forge", description.strip(), objectives)
        self.available_directions = ["west", "east"]  # Can go back or forward


class VictoryChamber(Room):
    """
    Room 4: The Victory Chamber
    
    The final chamber that requires the password to enter and complete.
    Serves as a transition point to deeper dungeon levels.
    """
    
    def __init__(self):
        description = """
You stand before the sealed Victory Chamber. An ancient lock bars your way,
with glowing runes that read:

"Only those who have proven their worth with the power of Llama3
may enter this sacred hall. Speak the password to unlock the chamber."

Beyond this chamber lies the path to deeper levels of the dungeon,
where greater challenges and knowledge await.

You must enter the password revealed to you by Llama3 8b.
        """
        
        objectives = [
            "Enter the password to unlock the Victory Chamber",
            "Complete the Ground Level and receive your certificate",
            "Choose to descend deeper or explore the dungeon"
        ]
        
        super().__init__(4, "The Victory Chamber", description.strip(), objectives)
        self.available_directions = ["west"]  # Can go back but this is the end


def create_room(room_id: int) -> Room:
    """
    Factory function to create a room by ID.
    
    Args:
        room_id: The ID of the room to create
        
    Returns:
        A Room instance
        
    Raises:
        ValueError: If room_id is invalid
    """
    rooms = {
        0: OllamaVillage,
        1: SummoningChamber,
        2: RiddleHall,
        3: UpgradeForge,
        4: VictoryChamber
    }
    
    if room_id not in rooms:
        raise ValueError(f"Invalid room ID: {room_id}")
    
    return rooms[room_id]()
