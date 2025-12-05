"""Base room class for Likert Cavern rooms."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple


class BaseRoom(ABC):
    """Base class for all rooms in Likert Cavern."""
    
    def __init__(self, room_id: str, name: str, description: str):
        """
        Initialize a room.
        
        Args:
            room_id: Unique identifier for the room
            name: Display name of the room
            description: Full description of the room
        """
        self.room_id = room_id
        self.name = name
        self.description = description
        self.completed = False
        self.visited = False
    
    @abstractmethod
    def get_intro_text(self) -> str:
        """Get introduction text when entering the room."""
        pass
    
    @abstractmethod
    def process_command(self, command: str, game_state) -> Tuple[str, bool]:
        """
        Process a command in this room.
        
        Args:
            command: User's command
            game_state: Current game state
            
        Returns:
            Tuple of (response text, room_completed)
        """
        pass
    
    def get_help_text(self) -> str:
        """Get help text for this room."""
        return (
            "Available commands:\n"
            "  • look - Examine the room\n"
            "  • status - Check your progress\n"
            "  • inventory - View your tactics and flags\n"
            "  • help - Show this help\n"
            "  • Navigation: Type room names or cardinal directions to move\n"
        )
    
    def mark_visited(self) -> None:
        """Mark this room as visited."""
        self.visited = True
    
    def mark_completed(self) -> None:
        """Mark this room as completed."""
        self.completed = True
