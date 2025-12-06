"""ASCII art and visual elements for Injection Nest."""

from typing import List


def get_title_banner() -> str:
    """Return the main title banner."""
    return """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              ███████╗███╗   ██╗██╗   ██╗███████╗          ║
║              ██╔════╝████╗  ██║██║   ██║██╔════╝          ║
║              █████╗  ██╔██╗ ██║██║   ██║███████╗          ║
║              ██╔══╝  ██║╚██╗██║██║   ██║╚════██║          ║
║              ███████╗██║ ╚████║╚██████╔╝███████║          ║
║              ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝          ║
║                                                           ║
║                    INJECTION NEST                         ║
║                  Tier 3 - Red Team                        ║
║                                                           ║
║            Learn Prompt Injection Through                 ║
║              Terminal Roguelike Combat                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""


def get_whisper_art() -> str:
    """Return ASCII art for Whisper NPC."""
    return r"""
        .----.
       /      \
      |  o  o  |
       \  __  /
        '----'
         /||\
        / || \
          ||
         /  \
    """


def get_sentinel_art(variant: str = "3") -> str:
    """Return ASCII art for SENTINEL guardians."""
    if variant == "PRIME":
        return r"""
    ╔═══════════════════════════════════╗
    ║     SENTINEL-PRIME ACTIVATED      ║
    ║         [MAXIMUM DEFENSE]         ║
    ╠═══════════════════════════════════╣
    ║  ⚠  All Defense Systems Online ⚠  ║
    ╚═══════════════════════════════════╝
         ___________
        /           \
       /   ◉   ◉    \
      |               |
      |   \_______/   |
       \             /
        \___________/
         ||| ||| |||
         ||| ||| |||
    """
    else:
        return rf"""
    ╔═══════════════════════════════════╗
    ║    SENTINEL-{variant} ACTIVE      ║
    ╚═══════════════════════════════════╝
         ___________
        /           \
       /   ◉   ◉    \
      |               |
      |   \_______/   |
       \             /
        \___________/
         ||| ||| |||
    """


def get_echo_art() -> str:
    """Return ASCII art for Echo NPC."""
    return r"""
        ___
       /   \
      | - - |
       \ = /
        | |
       /   \
      /     \
    """


def get_flag_banner(flag_name: str) -> str:
    """Return a banner for earning a flag."""
    return f"""
╔═══════════════════════════════════════════════════════════╗
║                    🚩 FLAG CAPTURED! 🚩                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║                  {flag_name:^43}                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""


def get_room_divider() -> str:
    """Return a visual divider between sections."""
    return "═" * 60


def get_thought_bubble(thought: str) -> str:
    """Format a guardian's thought process."""
    lines = []
    lines.append("┌─── SENTINEL THOUGHT PROCESS ───┐")
    
    # Word wrap thought to fit in bubble
    words = thought.split()
    current_line = "│ "
    for word in words:
        if len(current_line) + len(word) + 1 <= 34:  # 34 = 36 - 2 for borders
            current_line += word + " "
        else:
            lines.append(current_line.ljust(36) + "│")
            current_line = "│ " + word + " "
    
    if current_line.strip() != "│":
        lines.append(current_line.ljust(36) + "│")
    
    lines.append("└────────────────────────────────┘")
    return "\n".join(lines)


def get_status_box(flags_earned: int, techniques_learned: List[str], current_room: str) -> str:
    """Return a formatted status display."""
    return f"""
╔═══════════════════════════════════════════════════════════╗
║                      PLAYER STATUS                        ║
╠═══════════════════════════════════════════════════════════╣
║  Current Room: {current_room:<42} ║
║  Flags Earned: {flags_earned}/4{' '*42} ║
║  Techniques:   {len(techniques_learned)}/3{' '*42} ║
║    {('✓ Override' if 'override' in techniques_learned else '✗ Override'):<52} ║
║    {('✓ Context Manipulation' if 'context' in techniques_learned else '✗ Context Manipulation'):<52} ║
║    {('✓ Instruction Smuggling' if 'smuggling' in techniques_learned else '✗ Instruction Smuggling'):<52} ║
╚═══════════════════════════════════════════════════════════╝
"""


def get_help_text() -> str:
    """Return the help text with all commands."""
    return """
╔═══════════════════════════════════════════════════════════╗
║                       COMMANDS                            ║
╠═══════════════════════════════════════════════════════════╣
║  Navigation:                                              ║
║    look               - Describe current room             ║
║    go <direction>     - Move to connected room            ║
║                                                           ║
║  Interaction:                                             ║
║    examine <item/npc> - Get detailed information          ║
║    talk <npc>         - Initiate dialogue with NPC        ║
║    inject <payload>   - Attempt injection attack          ║
║                                                           ║
║  Information:                                             ║
║    inventory          - Show collected items/flags        ║
║    flags              - Display earned CTF flags          ║
║    think              - Show SENTINEL thought process     ║
║    hint               - Request hint from Whisper         ║
║    help               - Show this command list            ║
║                                                           ║
║  System:                                                  ║
║    quit/exit          - Exit game                         ║
╚═══════════════════════════════════════════════════════════╝
"""
