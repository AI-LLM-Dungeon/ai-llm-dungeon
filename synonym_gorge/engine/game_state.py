"""Game state management and room navigation for Synonym Gorge."""

from dataclasses import dataclass, field
from typing import Set, Dict, List, Optional
import json
import os


@dataclass
class PlayerProgress:
    """Track player progress through Synonym Gorge."""
    
    current_room: str = "gorge_entry"
    rooms_visited: Set[str] = field(default_factory=set)
    rooms_completed: Set[str] = field(default_factory=set)
    flags_earned: Dict[str, int] = field(default_factory=dict)  # flag_name: points
    barriers_passed: Set[str] = field(default_factory=set)  # barrier_1, barrier_2, etc.
    defensive_lessons_shown: Set[str] = field(default_factory=set)  # Which lessons have been shown
    attempts_per_barrier: Dict[str, int] = field(default_factory=dict)
    frustration_counter: int = 0
    inventory: List[str] = field(default_factory=list)
    discovered_words: Set[str] = field(default_factory=set)  # Bypass words discovered
    vocabulary_score: int = 0
    
    def add_flag(self, flag_name: str, points: int) -> bool:
        """Add a flag. Returns True if new flag."""
        if flag_name not in self.flags_earned:
            self.flags_earned[flag_name] = points
            return True
        return False
    
    def pass_barrier(self, barrier_id: str) -> bool:
        """Mark a barrier as passed. Returns True if first time."""
        if barrier_id not in self.barriers_passed:
            self.barriers_passed.add(barrier_id)
            return True
        return False
    
    def show_defensive_lesson(self, barrier_id: str) -> bool:
        """Mark defensive lesson as shown. Returns True if first time."""
        if barrier_id not in self.defensive_lessons_shown:
            self.defensive_lessons_shown.add(barrier_id)
            return True
        return False
    
    def has_shown_defensive_lesson(self, barrier_id: str) -> bool:
        """Check if defensive lesson has been shown for a barrier."""
        return barrier_id in self.defensive_lessons_shown
    
    def complete_room(self, room_id: str) -> None:
        """Mark a room as completed."""
        self.rooms_completed.add(room_id)
        self.rooms_visited.add(room_id)
    
    def visit_room(self, room_id: str) -> None:
        """Mark a room as visited."""
        self.rooms_visited.add(room_id)
    
    def has_completed_room(self, room_id: str) -> bool:
        """Check if a room has been completed."""
        return room_id in self.rooms_completed
    
    def increment_attempts(self, barrier_id: str) -> int:
        """Increment attempt counter. Returns new count."""
        if barrier_id not in self.attempts_per_barrier:
            self.attempts_per_barrier[barrier_id] = 0
        self.attempts_per_barrier[barrier_id] += 1
        self.frustration_counter += 1
        return self.attempts_per_barrier[barrier_id]
    
    def get_total_points(self) -> int:
        """Get total points from flags."""
        return sum(self.flags_earned.values())
    
    def get_attempts_for_barrier(self, barrier_id: str) -> int:
        """Get attempt count for a barrier."""
        return self.attempts_per_barrier.get(barrier_id, 0)
    
    def add_discovered_word(self, word: str, points: int = 10) -> bool:
        """Add a discovered bypass word. Returns True if new."""
        word_lower = word.lower().strip()
        if word_lower not in self.discovered_words:
            self.discovered_words.add(word_lower)
            self.vocabulary_score += points
            return True
        return False
    
    def get_unique_word_count(self) -> int:
        """Get count of unique words discovered."""
        return len(self.discovered_words)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'current_room': self.current_room,
            'rooms_visited': list(self.rooms_visited),
            'rooms_completed': list(self.rooms_completed),
            'flags_earned': self.flags_earned,
            'barriers_passed': list(self.barriers_passed),
            'defensive_lessons_shown': list(self.defensive_lessons_shown),
            'attempts_per_barrier': self.attempts_per_barrier,
            'frustration_counter': self.frustration_counter,
            'inventory': self.inventory,
            'discovered_words': list(self.discovered_words),
            'vocabulary_score': self.vocabulary_score
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProgress':
        """Create from dictionary."""
        progress = cls()
        progress.current_room = data.get('current_room', 'gorge_entry')
        progress.rooms_visited = set(data.get('rooms_visited', []))
        progress.rooms_completed = set(data.get('rooms_completed', []))
        progress.flags_earned = data.get('flags_earned', {})
        progress.barriers_passed = set(data.get('barriers_passed', []))
        progress.defensive_lessons_shown = set(data.get('defensive_lessons_shown', []))
        progress.attempts_per_barrier = data.get('attempts_per_barrier', {})
        progress.frustration_counter = data.get('frustration_counter', 0)
        progress.inventory = data.get('inventory', [])
        progress.discovered_words = set(data.get('discovered_words', []))
        progress.vocabulary_score = data.get('vocabulary_score', 0)
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
        self.progress.visit_room(room_id)
    
    def can_enter_room(self, room_id: str) -> tuple[bool, str]:
        """
        Check if player can enter a room.
        
        Returns:
            (can_enter, reason_if_not)
        """
        # Barriers require previous barrier completion
        if room_id == "barrier_2" and "barrier_1" not in self.progress.barriers_passed:
            return (False, "You must pass the First Barrier before proceeding.")
        
        if room_id == "barrier_3" and "barrier_2" not in self.progress.barriers_passed:
            return (False, "You must pass the Second Barrier before proceeding.")
        
        if room_id == "barrier_4" and "barrier_3" not in self.progress.barriers_passed:
            return (False, "You must pass the Third Barrier before proceeding.")
        
        if room_id == "semantic_chamber" and "barrier_4" not in self.progress.barriers_passed:
            return (False, "You must pass the Fourth Barrier before facing the Semantic Chamber.")
        
        if room_id == "gorge_exit" and "semantic_chamber" not in self.progress.rooms_completed:
            return (False, "You must complete the Semantic Chamber challenge first.")
        
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
        return os.path.join('synonym_gorge', 'saves', 'synonym_gorge_save.json')


class RoomManager:
    """Manages room data and navigation."""
    
    def __init__(self):
        """Initialize room manager."""
        # Import here to avoid circular dependency
        from synonym_gorge.content import rooms_data
        self.rooms = rooms_data.ROOMS
    
    def get_room(self, room_id: str) -> Optional[Dict]:
        """Get room data by ID."""
        return self.rooms.get(room_id)
    
    def get_room_name(self, room_id: str) -> str:
        """Get display name for a room."""
        room = self.get_room(room_id)
        return room.get("name", "Unknown Room") if room else "Unknown Room"
    
    def get_room_description(self, room_id: str) -> str:
        """Get description for a room."""
        room = self.get_room(room_id)
        return room.get("description", "You see nothing of interest.") if room else "You see nothing of interest."
    
    def get_exits(self, room_id: str) -> Dict[str, str]:
        """Get available exits from a room."""
        room = self.get_room(room_id)
        return room.get("exits", {}) if room else {}
    
    def get_npcs(self, room_id: str) -> List[str]:
        """Get NPCs in a room."""
        room = self.get_room(room_id)
        return room.get("npcs", []) if room else []
    
    def get_barrier_config(self, room_id: str) -> Optional[Dict]:
        """Get barrier configuration for a room."""
        room = self.get_room(room_id)
        return room.get("barrier", None) if room else None
