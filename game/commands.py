"""
Shared command infrastructure for all levels.

This module provides standard command implementations that all levels
should use to ensure a consistent player experience.
"""

from typing import Dict, List, Optional, Any
import json
import os


# Standard help text constants
STANDARD_NAVIGATION_COMMANDS = """NAVIGATION:
  look, l                  - Examine your surroundings
  go <direction>           - Move in a direction
  <direction>              - Shortcut for go (e.g., 'north', 'east')
  ls                       - List available exits and destinations
  pwd                      - Show map with your current position marked
  map                      - Display full level map"""

STANDARD_INFO_COMMANDS = """INFORMATION:
  status                   - Show progress and current location
  inventory, inv, i        - Show collected items
  help, h, ?               - Show this help"""

STANDARD_SYSTEM_COMMANDS = """SYSTEM:
  save                     - Save your progress
  load                     - Load saved progress
  quit, exit, q            - Exit the game"""


class StandardCommands:
    """
    Base class providing standard command implementations.
    
    Levels can inherit from this class or use its methods directly
    to implement standard commands consistently.
    """
    
    def format_help(self, level_specific_commands: str = "", tips: str = "") -> str:
        """
        Format help text combining standard and level-specific commands.
        
        Args:
            level_specific_commands: Optional level-specific command section
            tips: Optional tips section
            
        Returns:
            Formatted help text string
        """
        help_text = """
╔═══════════════════════════════════════════════════════════════════════╗
║                            COMMAND HELP                               ║
╚═══════════════════════════════════════════════════════════════════════╝

"""
        help_text += STANDARD_NAVIGATION_COMMANDS + "\n\n"
        
        if level_specific_commands:
            help_text += level_specific_commands + "\n\n"
        
        help_text += STANDARD_INFO_COMMANDS + "\n\n"
        help_text += STANDARD_SYSTEM_COMMANDS + "\n"
        
        if tips:
            help_text += "\n" + tips + "\n"
        
        return help_text
    
    def list_exits(self, room_data: Dict[str, Any], room_manager: Any) -> None:
        """
        List available exits from the current room.
        
        Args:
            room_data: Current room data dictionary (must have 'exits' key)
            room_manager: Room manager instance with get_room method
        """
        exits = room_data.get('exits', {})
        
        if not exits:
            print("\nNo exits available from this room.\n")
            return
        
        print("\nAvailable directions:")
        for direction, destination_id in exits.items():
            destination_room = room_manager.get_room(destination_id)
            destination_name = destination_room.get('name', destination_id) if destination_room else destination_id
            print(f"  {direction} -> {destination_name}")
        print()
    
    def show_position_map(
        self,
        current_room: str,
        room_map: Dict[str, str],
        map_layout: List[str]
    ) -> None:
        """
        Show ASCII map with current position marked.
        
        Args:
            current_room: ID of the current room
            room_map: Dictionary mapping room IDs to display labels
            map_layout: List of strings defining the ASCII art map
        """
        print()
        for line in map_layout:
            output_line = line
            # Replace room labels with marked version if current
            for room_id, label in room_map.items():
                if room_id == current_room:
                    output_line = output_line.replace(f"[{label}]", f"[{label}*]")
            print(output_line)
        print()
    
    def show_status(self, progress: Any) -> None:
        """
        Show player status.
        
        Args:
            progress: Progress/PlayerProgress object with get_status method
        """
        if hasattr(progress, 'get_status'):
            print(progress.get_status())
        else:
            print("Status information not available.")
    
    def save_game(self, game_state: Any, save_path: str) -> None:
        """
        Save game progress to file.
        
        Args:
            game_state: Game state object with save_to_file method
            save_path: Path to save file
        """
        try:
            if hasattr(game_state, 'save_to_file'):
                game_state.save_to_file(save_path)
                print(f"\n✅ Game saved to {save_path}\n")
            else:
                # Fallback to manual JSON saving
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'w') as f:
                    json.dump(game_state.__dict__, f, indent=2)
                print(f"\n✅ Game saved to {save_path}\n")
        except Exception as e:
            print(f"\n❌ Error saving game: {e}\n")
    
    def load_game(self, game_state_class: Any, save_path: str) -> Optional[Any]:
        """
        Load game progress from file.
        
        Args:
            game_state_class: Game state class with load_from_file method
            save_path: Path to save file
            
        Returns:
            Loaded game state or None if load failed
        """
        try:
            if not os.path.exists(save_path):
                print(f"\n❌ No saved game found at {save_path}\n")
                return None
            
            if hasattr(game_state_class, 'load_from_file'):
                loaded_state = game_state_class.load_from_file(save_path)
                print(f"\n✅ Game loaded from {save_path}\n")
                return loaded_state
            else:
                # Fallback to manual JSON loading
                with open(save_path, 'r') as f:
                    data = json.load(f)
                print(f"\n✅ Game loaded from {save_path}\n")
                return data
        except Exception as e:
            print(f"\n❌ Error loading game: {e}\n")
            return None


# Utility function for levels that don't use the class directly
def format_standard_help(level_specific_commands: str = "", tips: str = "") -> str:
    """
    Convenience function to format help text without instantiating StandardCommands.
    
    Args:
        level_specific_commands: Optional level-specific command section
        tips: Optional tips section
        
    Returns:
        Formatted help text string
    """
    commands = StandardCommands()
    return commands.format_help(level_specific_commands, tips)
