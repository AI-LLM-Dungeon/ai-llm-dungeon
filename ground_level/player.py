"""Player class for the Ground Level of AI-LLM-Dungeon."""

from typing import Optional, Set
from .sidekick import Sidekick


class Player:
    """
    Represents the player character in the Ground Level.
    
    The player navigates rooms, manages sidekicks, earns knowledge points,
    and unlocks tips as they progress through the tutorial.
    
    Attributes:
        current_room (int): ID of the room the player is currently in
        active_sidekick (Optional[Sidekick]): The currently active sidekick, if any
        knowledge_points (int): Points earned by completing objectives
        unlocked_tips (Set[str]): Set of tip IDs that have been unlocked
        completed_objectives (Set[str]): Set of completed objective IDs
    """
    
    def __init__(self):
        """Initialize a new Player with default values."""
        self.current_room: int = 1  # Start in Room 1
        self.active_sidekick: Optional[Sidekick] = None
        self.knowledge_points: int = 0
        self.unlocked_tips: Set[str] = set()
        self.completed_objectives: Set[str] = set()
    
    def move_to_room(self, room_id: int) -> None:
        """
        Move the player to a different room.
        
        Args:
            room_id: The ID of the room to move to
        """
        self.current_room = room_id
    
    def set_active_sidekick(self, sidekick: Optional[Sidekick]) -> None:
        """
        Set the active sidekick for the player.
        
        Args:
            sidekick: The sidekick to activate, or None to deactivate
        """
        # Deactivate previous sidekick if any
        if self.active_sidekick:
            self.active_sidekick.active = False
        
        # Set new sidekick
        self.active_sidekick = sidekick
        
        if sidekick:
            sidekick.active = True
    
    def has_active_sidekick(self) -> bool:
        """
        Check if the player has an active sidekick.
        
        Returns:
            True if there's an active sidekick, False otherwise
        """
        return self.active_sidekick is not None and self.active_sidekick.active
    
    def add_knowledge_points(self, points: int) -> None:
        """
        Award knowledge points to the player.
        
        Args:
            points: Number of points to add
        """
        self.knowledge_points += points
        print(f"\n⭐ +{points} Knowledge Points! (Total: {self.knowledge_points})")
    
    def unlock_tip(self, tip_id: str, tip_text: str) -> bool:
        """
        Unlock a new tip for the player.
        
        Args:
            tip_id: Unique identifier for the tip
            tip_text: The text content of the tip
            
        Returns:
            True if tip was newly unlocked, False if already unlocked
        """
        if tip_id in self.unlocked_tips:
            return False  # Already unlocked
        
        self.unlocked_tips.add(tip_id)
        
        # Display unlock notification
        from .ascii_art import display_tip_unlock
        display_tip_unlock(tip_text)
        
        return True
    
    def complete_objective(self, objective_id: str) -> None:
        """
        Mark an objective as completed.
        
        Args:
            objective_id: Unique identifier for the objective
        """
        self.completed_objectives.add(objective_id)
    
    def has_completed_objective(self, objective_id: str) -> bool:
        """
        Check if an objective has been completed.
        
        Args:
            objective_id: Unique identifier for the objective
            
        Returns:
            True if completed, False otherwise
        """
        return objective_id in self.completed_objectives
    
    def get_status(self) -> str:
        """
        Get a formatted status string for the player.
        
        Returns:
            A formatted status string showing player progress
        """
        status = f"\n{'='*50}\n"
        status += f"PLAYER STATUS\n"
        status += f"{'='*50}\n"
        status += f"Current Room: {self.current_room}\n"
        status += f"Knowledge Points: {self.knowledge_points}\n"
        status += f"Tips Unlocked: {len(self.unlocked_tips)}\n"
        
        if self.active_sidekick:
            status += f"Active Sidekick: {self.active_sidekick.name}\n"
        else:
            status += f"Active Sidekick: None\n"
        
        status += f"{'='*50}\n"
        
        return status
    
    def display_unlocked_tips(self, tips_data: dict) -> None:
        """
        Display all unlocked tips.
        
        Args:
            tips_data: Dictionary mapping tip IDs to tip data
        """
        if not self.unlocked_tips:
            print("\n📚 No tips unlocked yet. Keep exploring!\n")
            return
        
        print("\n📚 UNLOCKED KNOWLEDGE TIPS 📚\n")
        for tip_id in sorted(self.unlocked_tips):
            if tip_id in tips_data:
                tip = tips_data[tip_id]
                print(f"  💡 {tip['text']}")
        print()
    
    def can_proceed_to_room(self, room_id: int) -> tuple[bool, str]:
        """
        Check if the player can proceed to a specific room.
        
        Args:
            room_id: The ID of the room to check
            
        Returns:
            Tuple of (can_proceed: bool, reason: str)
        """
        # Room 2 requires completing room 1 objectives
        if room_id == 2 and not self.has_completed_objective("room1_complete"):
            return False, "You must complete the Summoning Chamber first!"
        
        # Room 3 requires completing room 2 objectives
        if room_id == 3 and not self.has_completed_objective("room2_complete"):
            return False, "You must complete the Riddle Hall first!"
        
        # Room 4 requires completing room 3 objectives
        if room_id == 4 and not self.has_completed_objective("room3_complete"):
            return False, "You must complete the Upgrade Forge first!"
        
        return True, ""
    
    def save_state(self) -> dict:
        """
        Save the player's state to a dictionary.
        
        Returns:
            Dictionary containing player state
        """
        return {
            "current_room": self.current_room,
            "knowledge_points": self.knowledge_points,
            "unlocked_tips": list(self.unlocked_tips),
            "completed_objectives": list(self.completed_objectives),
            "active_sidekick_name": self.active_sidekick.name if self.active_sidekick else None
        }
    
    def load_state(self, state: dict, sidekicks: dict) -> None:
        """
        Load the player's state from a dictionary.
        
        Args:
            state: Dictionary containing player state
            sidekicks: Dictionary of available sidekicks by name
        """
        self.current_room = state.get("current_room", 1)
        self.knowledge_points = state.get("knowledge_points", 0)
        self.unlocked_tips = set(state.get("unlocked_tips", []))
        self.completed_objectives = set(state.get("completed_objectives", []))
        
        # Restore active sidekick
        sidekick_name = state.get("active_sidekick_name")
        if sidekick_name and sidekick_name in sidekicks:
            self.set_active_sidekick(sidekicks[sidekick_name])
    
    def __str__(self) -> str:
        """String representation of the player."""
        return f"Player(Room {self.current_room}, {self.knowledge_points} KP)"
