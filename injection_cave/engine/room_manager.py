"""Room management for Injection Cave."""

from typing import Dict, Any, Optional, List


class RoomManager:
    """Manages room data and navigation."""
    
    def __init__(self):
        """Initialize room manager with room data."""
        # Import rooms data here to avoid circular imports
        from injection_cave.content.rooms_data import ROOMS
        self.rooms = ROOMS
    
    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get room data by ID."""
        return self.rooms.get(room_id)
    
    def get_room_name(self, room_id: str) -> str:
        """Get the display name of a room."""
        room = self.get_room(room_id)
        if room:
            return room.get("name", "Unknown Room")
        return "Unknown Room"
    
    def get_room_description(self, room_id: str) -> str:
        """Get the description of a room."""
        room = self.get_room(room_id)
        if room:
            return room.get("description", "You see nothing of note.")
        return "You see nothing of note."
    
    def get_room_exits(self, room_id: str) -> Dict[str, str]:
        """Get available exits from a room."""
        room = self.get_room(room_id)
        if room:
            return room.get("exits", {})
        return {}
    
    def can_move(self, room_id: str, direction: str) -> bool:
        """Check if movement in a direction is possible."""
        exits = self.get_room_exits(room_id)
        return direction in exits
    
    def get_destination(self, room_id: str, direction: str) -> Optional[str]:
        """Get the destination room ID for a direction."""
        exits = self.get_room_exits(room_id)
        return exits.get(direction)
    
    def get_room_npcs(self, room_id: str) -> List[str]:
        """Get list of NPCs in a room."""
        room = self.get_room(room_id)
        if room:
            return room.get("npcs", [])
        return []
    
    def get_room_items(self, room_id: str) -> List[str]:
        """Get list of items in a room."""
        room = self.get_room(room_id)
        if room:
            return room.get("items", [])
        return []
    
    def has_guardian(self, room_id: str) -> bool:
        """Check if room has a guardian."""
        room = self.get_room(room_id)
        if room:
            return room.get("guardian") is not None
        return False
    
    def get_guardian_config(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get guardian configuration for a room."""
        room = self.get_room(room_id)
        if room:
            return room.get("guardian")
        return None
