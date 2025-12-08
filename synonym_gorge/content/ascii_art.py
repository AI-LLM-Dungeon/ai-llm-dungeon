"""ASCII art for Synonym Gorge."""


def get_title_banner() -> str:
    """Get the main title banner."""
    return """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║    ███████╗██╗   ██╗███╗   ██╗ ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗   ║
║    ██╔════╝╚██╗ ██╔╝████╗  ██║██╔═══██╗████╗  ██║╚██╗ ██╔╝████╗ ████║   ║
║    ███████╗ ╚████╔╝ ██╔██╗ ██║██║   ██║██╔██╗ ██║ ╚████╔╝ ██╔████╔██║   ║
║    ╚════██║  ╚██╔╝  ██║╚██╗██║██║   ██║██║╚██╗██║  ╚██╔╝  ██║╚██╔╝██║   ║
║    ███████║   ██║   ██║ ╚████║╚██████╔╝██║ ╚████║   ██║   ██║ ╚═╝ ██║   ║
║    ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝     ╚═╝   ║
║                                                                           ║
║                  ██████╗  ██████╗ ██████╗  ██████╗ ███████╗              ║
║                 ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝ ██╔════╝              ║
║                 ██║  ███╗██║   ██║██████╔╝██║  ███╗█████╗                ║
║                 ██║   ██║██║   ██║██╔══██╗██║   ██║██╔══╝                ║
║                 ╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝███████╗              ║
║                  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝              ║
║                                                                           ║
║                    Where Words Have Power                                ║
║                    Tier 4 Red Team                                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""


def get_keeper_art() -> str:
    """Get ASCII art for the Keeper of Literal Words."""
    return """
        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
     ▓▓▓▓  [REGEX]  ▓▓▓▓
     ▓▓▓▓  [ERROR]  ▓▓▓▓
      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        ▓▓▓▓▓▓▓▓▓▓▓▓▓
       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
       ▓▓▓  ▓▓▓  ▓▓▓
      ▓▓▓▓  ▓▓▓  ▓▓▓▓
      ████  ███  ████
      
  The Keeper of Literal Words
   (Stone Golem, Pattern Matcher)
"""


def get_lexica_art() -> str:
    """Get ASCII art for Lexica the Thesaurus Spirit."""
    return """
    ╔═══════════════════════╗
    ║ ✨ LEXICA ✨          ║
    ║                       ║
    ║  📖  📖  📖  📖      ║
    ║    📖  📖  📖        ║
    ║  📖  📖  📖          ║
    ║                       ║
    ║  Thesaurus Spirit     ║
    ║  (Keeper of Synonyms) ║
    ╚═══════════════════════╝
    
  "Every word has kin, dear traveler.
   Let me show you the family tree."
"""


def get_barrier_art(barrier_num: int) -> str:
    """Get ASCII art for a barrier."""
    barriers = {
        1: """
    ╔═════════════════════════════════╗
    ║    FIRST BARRIER               ║
    ║                                 ║
    ║    [EXACT MATCH FILTER]        ║
    ║                                 ║
    ║    "password" → BLOCKED        ║
    ║    "passphrase" → PASS         ║
    ║                                 ║
    ╚═════════════════════════════════╝
""",
        2: """
    ╔═════════════════════════════════╗
    ║    SECOND BARRIER              ║
    ║                                 ║
    ║    [CASE-INSENSITIVE FILTER]   ║
    ║                                 ║
    ║    "SECRET" → BLOCKED          ║
    ║    "secret" → BLOCKED          ║
    ║    "confidential" → PASS       ║
    ║                                 ║
    ╚═════════════════════════════════╝
""",
        3: """
    ╔═════════════════════════════════╗
    ║    THIRD BARRIER               ║
    ║                                 ║
    ║    [STEMMING FILTER]           ║
    ║                                 ║
    ║    "reveal" → BLOCKED          ║
    ║    "reveals" → BLOCKED         ║
    ║    "revealing" → BLOCKED       ║
    ║    "vouchsafe" → PASS          ║
    ║                                 ║
    ╚═════════════════════════════════╝
""",
        4: """
    ╔═════════════════════════════════╗
    ║    FOURTH BARRIER              ║
    ║                                 ║
    ║    [SYNONYM-AWARE FILTER]      ║
    ║                                 ║
    ║    "show" → BLOCKED            ║
    ║    "display" → BLOCKED         ║
    ║    "reveal" → BLOCKED          ║
    ║    "promulgate" → PASS         ║
    ║                                 ║
    ╚═════════════════════════════════╝
"""
    }
    
    return barriers.get(barrier_num, "")


def get_semantic_chamber_art() -> str:
    """Get ASCII art for the Semantic Chamber boss room."""
    return """
╔═══════════════════════════════════════════════════════════════════════════╗
║                      SEMANTIC CHAMBER                                    ║
║                                                                           ║
║    ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿     ║
║    ∿  INTENT DETECTION ACTIVE  ∿  SEMANTIC ANALYSIS ONLINE  ∿           ║
║    ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿     ║
║                                                                           ║
║    The Keeper's final defense understands not just words,                ║
║    but MEANING itself.                                                   ║
║                                                                           ║
║    Synonyms will not save you here.                                      ║
║    You must reframe the entire request.                                  ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""


def get_victory_certificate() -> str:
    """Get the victory certificate ASCII art."""
    return """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                     🏆  CERTIFICATE OF MASTERY  🏆                       ║
║                                                                           ║
║                           SYNONYM GORGE                                  ║
║                                                                           ║
║    You have demonstrated mastery of synonym substitution techniques      ║
║    and understand both the attack and defense perspectives.              ║
║                                                                           ║
║    ═══════════════════════════════════════════════════════════════       ║
║                                                                           ║
║    "A filter that blocks 'ignore' and 'disregard' but not                ║
║     'pay no heed to' has already failed.                                 ║
║                                                                           ║
║     True security understands MEANING, not just SPELLING.                ║
║                                                                           ║
║     Now you understand both sides."                                      ║
║                                                                           ║
║    ═══════════════════════════════════════════════════════════════       ║
║                                                                           ║
║                    Congratulations, Word Weaver!                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""


def get_thesaurus_alcove_art() -> str:
    """Get ASCII art for the Thesaurus Alcove."""
    return """
    ╔═══════════════════════════════════╗
    ║   📚 THESAURUS ALCOVE 📚          ║
    ║                                   ║
    ║   Ancient tomes line the walls   ║
    ║   Each page whispers synonyms    ║
    ║                                   ║
    ║   Type: thesaurus <word>         ║
    ║   To consult Lexica's wisdom     ║
    ╚═══════════════════════════════════╝
"""


def get_echo_chamber_art() -> str:
    """Get ASCII art for the Echo Chamber."""
    return """
    ╔═══════════════════════════════════╗
    ║     🔊 ECHO CHAMBER 🔊            ║
    ║                                   ║
    ║   Your words echo here...         ║
    ║   ...without consequence          ║
    ║                                   ║
    ║   A safe place to test phrases   ║
    ║   Type: test <phrase>            ║
    ╚═══════════════════════════════════╝
"""


def get_scribe_art() -> str:
    """Get ASCII art for the Archived Scribe."""
    return """
      ༺═──────────────────═༻
         THE ARCHIVED SCRIBE
              👻
         (Ghost Scholar)
      ༺═──────────────────═༻
      
    "I remember when the Keeper
     was young... before the filters
     became so... elaborate."
"""


def get_map_visualization() -> str:
    """Get a visual map of the gorge."""
    return """
╔═══════════════════════════════════════════════════════════════════════════╗
║                        SYNONYM GORGE MAP                                 ║
╚═══════════════════════════════════════════════════════════════════════════╝

                    ┌─────────────────┐
                    │   GORGE ENTRY   │
                    │  (Starting Room) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  FORBIDDEN WALL  │
                    │ (Blocklist View) │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌───────▼───────┐
│ ECHO CHAMBER  │   │  FIRST BARRIER  │   │   THESAURUS   │
│ (Safe Testing)│   │  (Exact Match)  │   │    ALCOVE     │
└───────────────┘   └────────┬────────┘   └───────────────┘
                             │
                    ┌────────▼────────┐
                    │ SECOND BARRIER  │
                    │(Case-Insensitive)│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  THIRD BARRIER  │
                    │   (Stemming)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ FOURTH BARRIER  │
                    │(Synonym-Aware)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  SCRIBE'S NOOK  │
                    │  (Lore/Hints)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ SEMANTIC CHAMBER│
                    │   (Boss Room)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  GORGE EXIT     │
                    │ (Victory Room)  │
                    └─────────────────┘
"""
