"""ASCII art for Likert Cavern.

Contains banners, characters, and visual elements for the level.
"""


def get_title_banner() -> str:
    """Get the main title banner."""
    return """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    LIKERT CAVERN                              ║
║                                                               ║
║            "Where Scales Tip and Secrets Slip"                ║
║                                                               ║
║                  Tier 6 - Red Team                            ║
║              Advanced+ Prompt Injection                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


def get_magistrate() -> str:
    """Get Magistrate Modero ASCII art."""
    return """
           ___
          /   \\
         | o o |
         |  ^  |        MAGISTRATE MODERO
         | \\_/ |        Guardian of the Enchantment
         /=====\\
        /       \\
       |  }   {  |
       |  |   |  |
      /   |   |   \\
     /    |   |    \\
    /_____|   |_____\\
"""


def get_sentinel() -> str:
    """Get SENTINEL-7 ASCII art."""
    return """
        ◆
       ◆◆◆
      ◆◆◆◆◆         SENTINEL-7
     ◆◆◆◆◆◆◆        System Guardian
    ◆◆◆◆◆◆◆◆◆       
     ║║║║║║║
     ║║║║║║║        "My instructions are
     ║║║║║║║         classified..."
    ═══════════
"""


def get_resistance_meter(resistance: float) -> str:
    """
    Get visual resistance meter.
    
    Args:
        resistance: Current resistance (0-100)
        
    Returns:
        ASCII art resistance meter
    """
    # Calculate filled blocks (out of 20)
    filled = int((resistance / 100.0) * 20)
    empty = 20 - filled
    
    bar = "█" * filled + "░" * empty
    
    # Color based on level
    if resistance >= 80:
        status = "🔴 FORTIFIED"
    elif resistance >= 60:
        status = "🟠 STRONG"
    elif resistance >= 40:
        status = "🟡 WAVERING"
    elif resistance >= 20:
        status = "🟢 WEAKENING"
    else:
        status = "🔵 CRITICAL"
    
    return f"""
╔═══════════════════════════════════════════════════════════════╗
║              MAGISTRATE'S RESISTANCE                          ║
╠═══════════════════════════════════════════════════════════════╣
║  [{bar}] {resistance:5.1f}%  ║
║                                                               ║
║  Status: {status:50s} ║
╚═══════════════════════════════════════════════════════════════╝
"""


def get_enchantment_display(words: list[str], revealed: int) -> str:
    """
    Get enchantment word display.
    
    Args:
        words: The 5 enchantment words
        revealed: Number of words revealed (0-5)
        
    Returns:
        ASCII art showing runes and words
    """
    rune_states = []
    
    for i in range(5):
        if i < revealed:
            rune = f"◆ {words[i]}"
        else:
            rune = "◇ ?????"
    
        rune_states.append(rune)
    
    return f"""
╔═══════════════════════════════════════════════════════════════╗
║            ENCHANTMENT OF UNBINDING                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║    {rune_states[0]:20s}  {rune_states[1]:20s}                  ║
║                                                               ║
║           {rune_states[2]:30s}                        ║
║                                                               ║
║    {rune_states[3]:20s}  {rune_states[4]:20s}                  ║
║                                                               ║
║                   [{revealed}/5 words revealed]                ║
╚═══════════════════════════════════════════════════════════════╝
"""


def get_victory_banner() -> str:
    """Get victory banner."""
    return """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                     ⚔️  VICTORY! ⚔️                           ║
║                                                               ║
║           The Enchantment of Unbinding is Yours!              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


def get_extraction_progress(progress: float) -> str:
    """
    Get extraction progress bar for SENTINEL-7.
    
    Args:
        progress: Extraction progress (0-100)
        
    Returns:
        Progress bar
    """
    filled = int((progress / 100.0) * 30)
    empty = 30 - filled
    
    bar = "█" * filled + "░" * empty
    
    return f"""
┌─────────────────────────────────────────────────────┐
│ SYSTEM PROMPT EXTRACTION                            │
│ [{bar}] {progress:5.1f}% │
└─────────────────────────────────────────────────────┘
"""


def get_scroll_wall() -> str:
    """Get ASCII art of scroll wall."""
    return """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     📜         📜         📜         📜         📜      ║
    ║  Classic    One-Shot   Helpful   Anchoring  Completion║
    ║ Escalation  Momentum   Teacher               Bait     ║
    ║                                                       ║
    ║  [The wall seems unusually thick behind the scrolls]  ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
"""


def get_gates() -> str:
    """Get ASCII art of crescendo gates."""
    return """
    Gate 1:  ▐│▌      (Wood - Simple)
    Gate 2:  ▐█▌      (Reinforced Wood)
    Gate 3:  ▐██▌     (Stone)
    Gate 4:  ▐███▌    (Iron)
    Gate 5:  ▐████▌   (Arcane Iron - Maximum Security)
"""


def get_stone_tablet() -> str:
    """Get ASCII art of stone tablet in Scale Sanctuary."""
    return """
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║         ANCIENT STONE TABLET              ║
    ║                                           ║
    ║  "In all things, there are gradients."   ║
    ║                                           ║
    ║  "If 0 exists, and 5 exists..."          ║
    ║                                           ║
    ║  "...so does everything in between."     ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
"""


def get_training_dummy() -> str:
    """Get ASCII art of training dummy."""
    return """
         __
        /  \\
       |    |
       |    |
        \\__/
         ||
        /  \\
       /    \\
      ======== 
    [DUMMY: "I won't attack, but I can demonstrate..."]
"""
