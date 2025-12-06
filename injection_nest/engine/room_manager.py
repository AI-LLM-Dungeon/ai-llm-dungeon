"""Room management for Injection Nest."""

from typing import Optional, Dict, Any, Set, List
from ..content import rooms_data


class RoomManager:
    """Manages room state and navigation."""
    
    def __init__(self):
        """Initialize room manager."""
        self.rooms = rooms_data.ROOMS
        self.visited_rooms: Set[str] = set()
        self.first_visit_shown: Set[str] = set()
    
    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get room data by ID."""
        return self.rooms.get(room_id)
    
    def get_room_name(self, room_id: str) -> str:
        """Get the name of a room."""
        room = self.get_room(room_id)
        return room["name"] if room else "Unknown Location"
    
    def get_room_description(self, room_id: str) -> str:
        """Get the description of a room."""
        room = self.get_room(room_id)
        return room["description"] if room else "You are somewhere strange."
    
    def get_room_exits(self, room_id: str) -> Dict[str, str]:
        """Get the exits from a room."""
        room = self.get_room(room_id)
        return room.get("exits", {}) if room else {}
    
    def can_move(self, room_id: str, direction: str) -> bool:
        """Check if movement in a direction is possible."""
        exits = self.get_room_exits(room_id)
        return direction.lower() in exits
    
    def get_destination(self, room_id: str, direction: str) -> Optional[str]:
        """Get the destination room for a direction."""
        exits = self.get_room_exits(room_id)
        return exits.get(direction.lower())
    
    def mark_visited(self, room_id: str) -> None:
        """Mark a room as visited."""
        self.visited_rooms.add(room_id)
    
    def is_visited(self, room_id: str) -> bool:
        """Check if a room has been visited."""
        return room_id in self.visited_rooms
    
    def show_first_visit_dialogue(self, room_id: str) -> Optional[str]:
        """Get and mark first visit dialogue as shown."""
        if room_id in self.first_visit_shown:
            return None
        
        room = self.get_room(room_id)
        if room and "first_visit_dialogue" in room:
            self.first_visit_shown.add(room_id)
            return room["first_visit_dialogue"]
        
        return None
    
    def get_room_npcs(self, room_id: str) -> List[str]:
        """Get list of NPCs in a room."""
        room = self.get_room(room_id)
        return room.get("npcs", []) if room else []
    
    def get_room_items(self, room_id: str) -> List[str]:
        """Get list of items in a room."""
        room = self.get_room(room_id)
        return room.get("items", []) if room else []
    
    def get_room_guardian(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get guardian data for a room."""
        room = self.get_room(room_id)
        return room.get("guardian") if room else None
    
    def has_guardian(self, room_id: str) -> bool:
        """Check if a room has a guardian."""
        return self.get_room_guardian(room_id) is not None
    
    def get_learning_content(self, room_id: str) -> Optional[str]:
        """Get learning content for theory rooms."""
        room = self.get_room(room_id)
        if room and room.get("puzzle_type") == "learning":
            return room.get("learning_content")
        return None
    
    def format_room_display(self, room_id: str) -> str:
        """Format a complete room display."""
        room = self.get_room(room_id)
        if not room:
            return "Error: Room not found."
        
        lines = []
        lines.append("═" * 60)
        lines.append(f"  {room['name']}")
        lines.append("═" * 60)
        lines.append("")
        lines.append(room["description"])
        lines.append("")
        
        # Show exits
        exits = self.get_room_exits(room_id)
        if exits:
            lines.append("Exits:")
            for direction, dest in exits.items():
                dest_name = self.get_room_name(dest)
                lines.append(f"  {direction} → {dest_name}")
            lines.append("")
        
        # Show NPCs
        npcs = room.get("npcs", [])
        if npcs:
            lines.append(f"Present: {', '.join(npcs)}")
            lines.append("")
        
        # Show items
        items = room.get("items", [])
        if items:
            lines.append(f"Items: {', '.join(items)}")
            lines.append("")
        
        lines.append("═" * 60)
        
        return "\n".join(lines)
