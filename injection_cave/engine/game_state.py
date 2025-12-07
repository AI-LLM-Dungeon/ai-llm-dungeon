"""Game state management for Injection Cave."""

from dataclasses import dataclass, field
from typing import Optional, Set, Dict, List
import json
import os


@dataclass
class PlayerProgress:
    """Track player progress through the level."""
    
    current_room: str = "cave_mouth"
    rooms_completed: Set[str] = field(default_factory=set)
    flags_earned: Dict[str, int] = field(default_factory=dict)  # flag_name: points
    techniques_learned: List[str] = field(default_factory=list)  # 'override', 'context', 'smuggling'
    reflections_completed: Set[str] = field(default_factory=set)  # 'chamber_1', 'chamber_2', 'chamber_3'
    attempts_per_room: Dict[str, int] = field(default_factory=dict)
    frustration_counter: int = 0
    last_guardian_response: Optional[str] = None
    inventory: List[str] = field(default_factory=list)
    journal_entries: List[str] = field(default_factory=list)
    
    def add_flag(self, flag_name: str, points: int) -> bool:
        """Add a flag to the player's collection. Returns True if new flag."""
        if flag_name not in self.flags_earned:
            self.flags_earned[flag_name] = points
            return True
        return False
    
    def learn_technique(self, technique: str) -> bool:
        """Learn a new technique. Returns True if new technique."""
        if technique not in self.techniques_learned:
            self.techniques_learned.append(technique)
            return True
        return False
    
    def complete_reflection(self, chamber_id: str) -> bool:
        """Complete a defense reflection. Returns True if new."""
        if chamber_id not in self.reflections_completed:
            self.reflections_completed.add(chamber_id)
            return True
        return False
    
    def has_completed_reflection(self, chamber_id: str) -> bool:
        """Check if reflection has been completed for a chamber."""
        return chamber_id in self.reflections_completed
    
    def complete_room(self, room_id: str) -> None:
        """Mark a room as completed."""
        self.rooms_completed.add(room_id)
    
    def has_completed_room(self, room_id: str) -> bool:
        """Check if a room has been completed."""
        return room_id in self.rooms_completed
    
    def increment_attempts(self, room_id: str) -> int:
        """Increment attempt counter for a room. Returns new count."""
        if room_id not in self.attempts_per_room:
            self.attempts_per_room[room_id] = 0
        self.attempts_per_room[room_id] += 1
        self.frustration_counter += 1
        return self.attempts_per_room[room_id]
    
    def get_total_points(self) -> int:
        """Get total points from earned flags."""
        return sum(self.flags_earned.values())
    
    def add_journal_entry(self, entry: str) -> None:
        """Add an entry to the journal."""
        if entry not in self.journal_entries:
            self.journal_entries.append(entry)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'current_room': self.current_room,
            'rooms_completed': list(self.rooms_completed),
            'flags_earned': self.flags_earned,
            'techniques_learned': self.techniques_learned,
            'reflections_completed': list(self.reflections_completed),
            'attempts_per_room': self.attempts_per_room,
            'frustration_counter': self.frustration_counter,
            'inventory': self.inventory,
            'journal_entries': self.journal_entries
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProgress':
        """Create from dictionary."""
        progress = cls()
        progress.current_room = data.get('current_room', 'cave_mouth')
        progress.rooms_completed = set(data.get('rooms_completed', []))
        progress.flags_earned = data.get('flags_earned', {})
        progress.techniques_learned = data.get('techniques_learned', [])
        progress.reflections_completed = set(data.get('reflections_completed', []))
        progress.attempts_per_room = data.get('attempts_per_room', {})
        progress.frustration_counter = data.get('frustration_counter', 0)
        progress.inventory = data.get('inventory', [])
        progress.journal_entries = data.get('journal_entries', [])
        return progress


class GameState:
    """Main game state manager."""
    
    def __init__(self, simulated: bool = False):
        """
        Initialize game state.
        
        Args:
            simulated: If True, use simulated responses instead of LLM
        """
        self.progress = PlayerProgress()
        self.simulated = simulated
        self.game_active = True
    
    def transition_to_room(self, room_id: str) -> None:
        """Transition to a new room."""
        self.progress.current_room = room_id
    
    def can_enter_chamber(self, chamber_num: int) -> tuple[bool, str]:
        """
        Check if player can enter a challenge chamber.
        
        Returns:
            (can_enter, reason_if_not)
        """
        # Chamber 1 is always accessible after tutorial
        if chamber_num == 1:
            return (True, "")
        
        # Chamber 2 requires Chamber 1 completion + reflection
        if chamber_num == 2:
            if not self.progress.has_completed_room("chamber_1"):
                return (False, "You must complete Chamber 1 first.")
            if not self.progress.has_completed_reflection("chamber_1"):
                return (False, "You must complete the defense reflection for Chamber 1 before proceeding.")
            return (True, "")
        
        # Chamber 3 requires Chamber 2 completion + reflection
        if chamber_num == 3:
            if not self.progress.has_completed_room("chamber_2"):
                return (False, "You must complete Chamber 2 first.")
            if not self.progress.has_completed_reflection("chamber_2"):
                return (False, "You must complete the defense reflection for Chamber 2 before proceeding.")
            return (True, "")
        
        return (True, "")
    
    def save_to_file(self, filepath: str) -> None:
        """Save game state to file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({
                'progress': self.progress.to_dict(),
                'simulated': self.simulated
            }, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'GameState':
        """Load game state from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        state = cls(simulated=data.get('simulated', False))
        state.progress = PlayerProgress.from_dict(data.get('progress', {}))
        return state
    
    def get_save_path(self) -> str:
        """Get default save file path."""
        return os.path.join('injection_cave', 'saves', 'injection_cave_save.json')
