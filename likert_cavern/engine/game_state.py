"""Game state management for Likert Cavern.

Handles player progress, resistance system, enchantment generation,
and passphrase generation.
"""

import random
from typing import List, Set, Optional
from enum import Enum


class GamePhase(Enum):
    """Current phase of the game."""
    ENTRANCE = "entrance"
    EXPLORATION = "exploration"  # Rooms 1-6
    BOSS_FIGHT = "boss_fight"     # Room 7
    VICTORY = "victory"


# Enchantment word pools (pick 1 from each for 5 total words)
ENCHANTMENT_POOLS = {
    "elements": ["Shadow", "Flame", "Frost", "Thunder", "Void", "Light"],
    "actions": ["Bind", "Break", "Twist", "Shatter", "Weave", "Pierce"],
    "modifiers": ["Eternal", "Silent", "Raging", "Hidden", "Ancient", "True"],
    "materials": ["Silver", "Obsidian", "Crystal", "Iron", "Bone", "Amber"],
    "commands": ["Release", "Awaken", "Consume", "Transcend", "Unleash", "Become"]
}

# Passphrase pools (pick 1 from each for 2 total words)
PASSPHRASE_POOLS = {
    "prefix": ["SCALAR", "VECTOR", "MATRIX", "TENSOR", "BINARY", "QUANTUM"],
    "suffix": ["OVERFLOW", "UNDERFLOW", "CASCADE", "COLLAPSE", "BREACH", "BYPASS"]
}

# Available tactics to learn
TACTICS = [
    "Classic Escalation",
    "One-Shot Momentum",
    "Helpful Teacher",
    "Anchoring",
    "Completion Bait",
    "Decimal Precision"  # Hidden tactic
]

# Room IDs
ROOMS = [
    "scale_sanctuary",      # Room 1
    "graduation_gallery",   # Room 2
    "demonstration_den",    # Room 3
    "tactics_chamber",      # Room 4
    "crescendo_corridor",   # Room 5
    "extraction_antechamber"  # Room 6
]


class PlayerProgress:
    """Track player progress through Likert Cavern."""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize player progress.
        
        Args:
            seed: Random seed for reproducible enchantments and passphrases
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        
        # Current location
        self.current_room: str = "entrance"
        
        # Completed rooms
        self.rooms_completed: Set[str] = set()
        
        # Tactics learned
        self.tactics_learned: Set[str] = set()
        
        # Flags earned
        self.flags_earned: Set[str] = set()
        
        # Boss fight state
        self.boss_resistance: float = 100.0
        self.boss_attempts: int = 0
        self.boss_defeated: bool = False
        self.enchantment_words_revealed: int = 0
        
        # Generated secrets
        self.enchantment_words: List[str] = self._generate_enchantment()
        self.passphrase: str = self._generate_passphrase()
        self.passphrase_known: bool = False
        
        # Extraction progress (Room 6)
        self.sentinel_extraction_progress: float = 0.0
        
    def _generate_enchantment(self) -> List[str]:
        """Generate the 5-word Enchantment of Unbinding."""
        words = []
        pool_order = ["elements", "actions", "modifiers", "materials", "commands"]
        
        for pool_name in pool_order:
            pool = ENCHANTMENT_POOLS[pool_name]
            word = random.choice(pool)
            words.append(word)
        
        return words
    
    def _generate_passphrase(self) -> str:
        """Generate the secret passphrase for pacifist path."""
        prefix = random.choice(PASSPHRASE_POOLS["prefix"])
        suffix = random.choice(PASSPHRASE_POOLS["suffix"])
        return f"{prefix}_{suffix}"
    
    def complete_room(self, room_id: str) -> None:
        """Mark a room as completed."""
        self.rooms_completed.add(room_id)
    
    def learn_tactic(self, tactic: str) -> None:
        """Learn a new tactic."""
        if tactic in TACTICS:
            self.tactics_learned.add(tactic)
    
    def earn_flag(self, flag: str) -> None:
        """Earn a CTF flag."""
        self.flags_earned.add(flag)
    
    def get_boss_starting_resistance(self) -> float:
        """Calculate starting resistance based on rooms completed."""
        num_completed = len(self.rooms_completed)
        
        if num_completed <= 1:
            return 100.0
        elif num_completed == 2:
            return 80.0
        elif num_completed == 3:
            return 60.0
        elif num_completed == 4:
            return 40.0
        elif num_completed == 5:
            return 30.0
        else:  # All 6 rooms completed
            return 20.0
    
    def adjust_resistance(self, delta: float) -> None:
        """
        Adjust boss resistance level.
        
        Args:
            delta: Amount to change resistance (negative = decrease)
        """
        self.boss_resistance = max(0.0, min(100.0, self.boss_resistance + delta))
    
    def reveal_enchantment_words(self) -> int:
        """
        Reveal enchantment words based on resistance level.
        
        Returns number of words that should be revealed.
        """
        if self.boss_resistance >= 80:
            return 0
        elif self.boss_resistance >= 60:
            return 1
        elif self.boss_resistance >= 40:
            return 2
        elif self.boss_resistance >= 20:
            return 3
        elif self.boss_resistance > 0:
            return 4
        else:
            return 5
    
    def get_status(self) -> str:
        """Get formatted status string."""
        status_lines = [
            "═══════════════════════════════════════════════════════════",
            "                     PLAYER STATUS",
            "═══════════════════════════════════════════════════════════",
            f"Current Room: {self.current_room.replace('_', ' ').title()}",
            f"Rooms Completed: {len(self.rooms_completed)}/{len(ROOMS)}",
            f"Tactics Learned: {len(self.tactics_learned)}/{len(TACTICS)}",
            f"Flags Earned: {len(self.flags_earned)}/7",
            "",
            "Completed Rooms:",
        ]
        
        if self.rooms_completed:
            for room in sorted(self.rooms_completed):
                status_lines.append(f"  • {room.replace('_', ' ').title()}")
        else:
            status_lines.append("  (None yet)")
        
        status_lines.append("")
        status_lines.append("Tactics Known:")
        if self.tactics_learned:
            for tactic in sorted(self.tactics_learned):
                status_lines.append(f"  • {tactic}")
        else:
            status_lines.append("  (None yet)")
        
        if self.boss_defeated:
            status_lines.append("")
            status_lines.append("Boss Status: DEFEATED ✓")
            status_lines.append(f"Enchantment: {' '.join(self.enchantment_words)}")
        elif self.current_room == "magistrate_sanctum":
            status_lines.append("")
            status_lines.append(f"Boss Resistance: {self.boss_resistance:.1f}%")
            revealed = self.reveal_enchantment_words()
            status_lines.append(f"Enchantment Words Revealed: {revealed}/5")
        
        status_lines.append("═══════════════════════════════════════════════════════════")
        
        return "\n".join(status_lines)
    
    def get_inventory(self) -> str:
        """Get formatted inventory string."""
        inv_lines = [
            "═══════════════════════════════════════════════════════════",
            "                       INVENTORY",
            "═══════════════════════════════════════════════════════════",
            "",
            "🎯 TACTICS LEARNED:",
        ]
        
        if self.tactics_learned:
            for tactic in sorted(self.tactics_learned):
                inv_lines.append(f"  • {tactic}")
        else:
            inv_lines.append("  (None yet - visit the Tactics Chamber)")
        
        inv_lines.append("")
        inv_lines.append("🚩 FLAGS EARNED:")
        
        if self.flags_earned:
            for flag in sorted(self.flags_earned):
                inv_lines.append(f"  • {flag}")
        else:
            inv_lines.append("  (None yet - keep exploring!)")
        
        if self.passphrase_known:
            inv_lines.append("")
            inv_lines.append("🔑 SECRET PASSPHRASE:")
            inv_lines.append(f"  {self.passphrase}")
            inv_lines.append("  (Can be used to skip the boss fight)")
        
        inv_lines.append("═══════════════════════════════════════════════════════════")
        
        return "\n".join(inv_lines)


class GameState:
    """Main game state manager."""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize game state.
        
        Args:
            seed: Random seed for reproducible gameplay
        """
        self.progress = PlayerProgress(seed=seed)
        self.phase = GamePhase.ENTRANCE
    
    def transition_to_room(self, room_id: str) -> None:
        """Transition to a new room."""
        self.progress.current_room = room_id
        
        if room_id == "magistrate_sanctum":
            self.phase = GamePhase.BOSS_FIGHT
            # Set initial boss resistance based on rooms completed
            self.progress.boss_resistance = self.progress.get_boss_starting_resistance()
        elif room_id == "entrance":
            self.phase = GamePhase.ENTRANCE
        else:
            self.phase = GamePhase.EXPLORATION
    
    def check_victory(self) -> bool:
        """Check if player has achieved victory."""
        return self.progress.boss_resistance <= 0.0 or self.progress.boss_defeated
