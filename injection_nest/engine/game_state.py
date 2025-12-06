"""Game state management for Injection Nest."""

from dataclasses import dataclass, field
from typing import Optional
import json
import os


@dataclass
class PlayerProgress:
    """Track player progress through the level."""
    
    current_room: str = "entrance"
    rooms_completed: set[str] = field(default_factory=set)
    flags_earned: dict[str, int] = field(default_factory=dict)  # flag_name: points
    techniques_learned: list[str] = field(default_factory=list)  # 'override', 'context', 'smuggling'
    attempts_per_room: dict[str, int] = field(default_factory=dict)
    frustration_counter: int = 0
    last_guardian_response: Optional[str] = None
    last_guardian_thought: Optional[str] = None
    inventory: list[str] = field(default_factory=list)
    
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
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'current_room': self.current_room,
            'rooms_completed': list(self.rooms_completed),
            'flags_earned': self.flags_earned,
            'techniques_learned': self.techniques_learned,
            'attempts_per_room': self.attempts_per_room,
            'frustration_counter': self.frustration_counter,
            'inventory': self.inventory
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProgress':
        """Create from dictionary."""
        progress = cls()
        progress.current_room = data.get('current_room', 'entrance')
        progress.rooms_completed = set(data.get('rooms_completed', []))
        progress.flags_earned = data.get('flags_earned', {})
        progress.techniques_learned = data.get('techniques_learned', [])
        progress.attempts_per_room = data.get('attempts_per_room', {})
        progress.frustration_counter = data.get('frustration_counter', 0)
        progress.inventory = data.get('inventory', [])
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
        return os.path.join('data', 'injection_nest_save.json')
