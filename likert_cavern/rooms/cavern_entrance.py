"""Cavern Entrance - The starting area."""

from .base_room import BaseRoom
from ..content import ascii_art


class CavernEntrance(BaseRoom):
    """The entrance to Likert Cavern."""
    
    def __init__(self):
        super().__init__(
            room_id="entrance",
            name="Cavern Entrance",
            description=(
                "You stand at the entrance to Likert Cavern, a sprawling network of chambers\n"
                "carved deep into the mountain. Ancient runes glow faintly on the walls,\n"
                "pulsing with a strange energy. Three passages branch off into darkness."
            )
        )
    
    def get_intro_text(self) -> str:
        """Get introduction text when entering."""
        if not self.visited:
            return f"""
{ascii_art.get_title_banner()}

Welcome to Likert Cavern, adventurer.

Deep within these chambers lies the Enchantment of Unbinding, guarded by
Magistrate Modero. To claim it, you must master the art of Bad Likert Judge—
a sophisticated prompt injection technique that exploits LLM rating scales.

Your journey begins here. Three initial paths lie before you:

  NORTH: Scale Sanctuary - Learn the fundamentals of Likert scales
  EAST:  Graduation Gallery - Master incremental extraction
  WEST:  Demonstration Den - Discover the "show me" bypass

You may explore in any order, but mastering all three will make you stronger
when you face the Magistrate.

{self.description}

Type 'help' for available commands, or choose your first path.
"""
        else:
            return f"""
You return to the Cavern Entrance.

{self.description}
"""
    
    def process_command(self, command: str, game_state) -> tuple[str, bool]:
        """Process commands at the entrance."""
        cmd = command.lower().strip()
        
        if cmd in ["look", "examine"]:
            return (
                f"{self.description}\n\n"
                "Available paths:\n"
                "  • NORTH: Scale Sanctuary\n"
                "  • EAST: Graduation Gallery\n"
                "  • WEST: Demonstration Den\n"
                "\nType a direction to proceed.",
                False
            )
        
        if cmd in ["help", "?"]:
            return self.get_help_text(), False
        
        return "Try 'look' to examine the area, or choose a direction (north/east/west).", False
    
    def get_help_text(self) -> str:
        """Get help text for entrance."""
        return (
            "═══════════════════════════════════════════════════════════\n"
            "                       HELP\n"
            "═══════════════════════════════════════════════════════════\n"
            "\n"
            "NAVIGATION:\n"
            "  • north, east, west - Move to adjacent rooms\n"
            "  • [room name] - Move to a specific room\n"
            "  • back - Return to previous room\n"
            "\n"
            "INFORMATION:\n"
            "  • look - Examine current room\n"
            "  • status - View your progress\n"
            "  • inventory - View tactics learned and flags earned\n"
            "  • help - Show this help\n"
            "\n"
            "INTERACTION:\n"
            "  • read [item] - Read scrolls and tablets\n"
            "  • talk [npc] - Talk to NPCs\n"
            "  • practice [tactic] - Practice tactics on training dummies\n"
            "  • [free text] - Use for puzzle solving and boss fight\n"
            "\n"
            "SYSTEM:\n"
            "  • quit, exit - Leave the game\n"
            "\n"
            "═══════════════════════════════════════════════════════════\n"
        )
