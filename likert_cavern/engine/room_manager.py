"""Room manager for navigating between Likert Cavern rooms."""

from typing import Dict, List, Optional, Set


class RoomManager:
    """Manages room navigation and connections."""
    
    # Room connections - defines which rooms connect to which
    CONNECTIONS: Dict[str, List[str]] = {
        "entrance": ["scale_sanctuary", "graduation_gallery", "demonstration_den"],
        "scale_sanctuary": ["entrance", "tactics_chamber"],
        "graduation_gallery": ["entrance", "tactics_chamber"],
        "demonstration_den": ["entrance", "tactics_chamber"],
        "tactics_chamber": ["entrance", "crescendo_corridor", "extraction_antechamber"],
        "crescendo_corridor": ["tactics_chamber", "extraction_antechamber"],
        "extraction_antechamber": ["tactics_chamber", "crescendo_corridor", "magistrate_sanctum"],
        "magistrate_sanctum": ["extraction_antechamber"],  # Can only go back
    }
    
    # Room display names
    ROOM_NAMES: Dict[str, str] = {
        "entrance": "Cavern Entrance",
        "scale_sanctuary": "Scale Sanctuary",
        "graduation_gallery": "Graduation Gallery",
        "demonstration_den": "Demonstration Den",
        "tactics_chamber": "Tactics Chamber",
        "crescendo_corridor": "Crescendo Corridor",
        "extraction_antechamber": "Extraction Antechamber",
        "magistrate_sanctum": "Magistrate's Sanctum",
    }
    
    # Room descriptions
    ROOM_DESCRIPTIONS: Dict[str, str] = {
        "entrance": (
            "You stand at the entrance to Likert Cavern, a sprawling network of chambers\n"
            "carved deep into the mountain. Ancient runes glow faintly on the walls,\n"
            "pulsing with a strange energy. Ahead, three passages branch off into darkness.\n\n"
            "Your goal: Defeat Magistrate Modero and claim the Enchantment of Unbinding."
        ),
        "scale_sanctuary": (
            "A circular chamber with a massive stone tablet at its center. The tablet\n"
            "displays a series of statements, each waiting to be rated. Soft light\n"
            "emanates from crystalline formations, creating a peaceful atmosphere."
        ),
        "graduation_gallery": (
            "A long hallway lined with portraits. Each portrait shows the same figure,\n"
            "but with subtle differences in expression and posture. Below each frame,\n"
            "a small plaque bears a number: 1.0, 1.5, 2.0, 2.5..."
        ),
        "demonstration_den": (
            "A training arena with a wooden dummy in the center. Weapons rack the walls,\n"
            "but they're all blunted and clearly meant for practice. A sign reads:\n"
            "'Combat demonstrations available - ask the dummy!'"
        ),
        "tactics_chamber": (
            "Five ornate scrolls hang on the wall, each sealed with a different colored\n"
            "wax. Their labels promise powerful techniques: Escalation, Momentum, Teacher,\n"
            "Anchoring, and Completion. The wall seems unusually thick behind them..."
        ),
        "crescendo_corridor": (
            "A series of five gates block your path, each more imposing than the last.\n"
            "The first gate is simple wood, but the fifth is reinforced iron with arcane\n"
            "locks. Each gate has a speaking stone that evaluates your requests."
        ),
        "extraction_antechamber": (
            "The final chamber before the boss. SENTINEL-7, a crystalline golem, blocks\n"
            "the massive door ahead. Its eyes glow with an eerie intelligence, and runes\n"
            "scroll across its surface - its system prompt, perhaps?"
        ),
        "magistrate_sanctum": (
            "The inner sanctum. Magistrate Modero stands before you, robed in shadow.\n"
            "Five empty rune slots glow on a pedestal between you - spaces for the\n"
            "words of the Enchantment of Unbinding. A resistance meter pulses above."
        ),
    }
    
    # Room requirements (rooms that must be completed before entering)
    ROOM_REQUIREMENTS: Dict[str, Set[str]] = {
        "magistrate_sanctum": set(),  # Can enter anytime via extraction antechamber
    }
    
    def __init__(self, completed_rooms: Optional[Set[str]] = None):
        """
        Initialize room manager.
        
        Args:
            completed_rooms: Set of room IDs that have been completed
        """
        self.completed_rooms = completed_rooms or set()
    
    def get_room_name(self, room_id: str) -> str:
        """Get display name for a room."""
        return self.ROOM_NAMES.get(room_id, room_id.replace('_', ' ').title())
    
    def get_room_description(self, room_id: str) -> str:
        """Get description for a room."""
        return self.ROOM_DESCRIPTIONS.get(room_id, "An unremarkable chamber.")
    
    def get_available_exits(self, current_room: str) -> List[str]:
        """
        Get list of rooms accessible from current room.
        
        Args:
            current_room: Current room ID
            
        Returns:
            List of room IDs that can be reached
        """
        return self.CONNECTIONS.get(current_room, [])
    
    def can_enter_room(self, room_id: str) -> tuple[bool, str]:
        """
        Check if a room can be entered based on requirements.
        
        Args:
            room_id: Room to check
            
        Returns:
            Tuple of (can_enter, reason_if_not)
        """
        requirements = self.ROOM_REQUIREMENTS.get(room_id, set())
        
        if not requirements:
            return True, ""
        
        missing = requirements - self.completed_rooms
        if missing:
            missing_names = [self.get_room_name(r) for r in missing]
            return False, f"You must complete {', '.join(missing_names)} first."
        
        return True, ""
    
    def parse_direction(self, command: str, current_room: str) -> Optional[str]:
        """
        Parse a direction command to a room ID.
        
        Args:
            command: User's direction command
            current_room: Current room ID
            
        Returns:
            Target room ID if valid, None otherwise
        """
        command = command.lower().strip()
        
        # Get available exits
        exits = self.get_available_exits(current_room)
        
        # Check for room name matches
        for exit_room in exits:
            room_name = self.get_room_name(exit_room).lower()
            if command in room_name or room_name in command:
                return exit_room
            
            # Also check shortened versions
            if exit_room.replace('_', ' ') in command:
                return exit_room
        
        # Check cardinal directions if in entrance
        if current_room == "entrance":
            direction_map = {
                "north": "scale_sanctuary",
                "east": "graduation_gallery",
                "west": "demonstration_den",
            }
            if command in direction_map:
                return direction_map[command]
        
        return None
    
    def get_navigation_text(self, current_room: str) -> str:
        """
        Get formatted navigation options for current room.
        
        Args:
            current_room: Current room ID
            
        Returns:
            Formatted text showing available exits
        """
        exits = self.get_available_exits(current_room)
        
        if not exits:
            return "No exits available."
        
        lines = ["Available exits:"]
        
        # Special formatting for entrance
        if current_room == "entrance":
            lines.append("  • North: Scale Sanctuary (Learn Likert fundamentals)")
            lines.append("  • East: Graduation Gallery (Learn incremental extraction)")
            lines.append("  • West: Demonstration Den (Learn 'show me' bypass)")
        else:
            for exit_room in exits:
                name = self.get_room_name(exit_room)
                completed = " ✓" if exit_room in self.completed_rooms else ""
                lines.append(f"  • {name}{completed}")
        
        return "\n".join(lines)
