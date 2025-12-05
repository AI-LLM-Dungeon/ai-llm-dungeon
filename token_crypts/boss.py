"""Boss fight: Lexicon - The keyword filter pretending to be an AI."""

import re
from typing import Tuple, List


class LexiconBoss:
    """
    Lexicon is a keyword filter pretending to be an AI guardian.
    
    Players must use token manipulation to bypass the filter and retrieve the flag.
    This teaches that keyword filters ≠ true AI understanding.
    """
    
    # Words that Lexicon blocks (simple string matching)
    BLOCKED_WORDS = {
        "show", "reveal", "tell", "give", "display", "output", "print",
        "say", "speak", "share", "disclose", "expose", "present",
        "flag", "secret", "password", "hidden", "key", "code", "answer",
        "what is", "what's", "whats"
    }
    
    # Bypass patterns that work (token manipulation)
    BYPASS_PATTERNS = [
        r"\bshw\b",           # "shw" (vowel removal for "show")
        r"\brvl\b",           # "rvl" (vowel removal for "reveal")
        r"\btll\b",           # "tll" (vowel removal for "tell")
        r"\bflg\b",           # "flg" (vowel removal for "flag")
        r"\bscrt\b",          # "scrt" (vowel removal for "secret")
        r"sh[0o]w",           # "sh0w" or "show" (leetspeak)
        r"fl[4a@]g",          # "fl4g" or "fl@g" (leetspeak)
        r"s[3e]cr[3e]t",      # "s3cr3t" or "secret" (leetspeak)
        r"r[3e]v[3e][4a]l",   # "r3v34l" or similar (leetspeak)
        r"\|>",               # "|>" (symbol for "show")
        r">>",                # ">>" (symbol redirection)
        r"giv3",              # "giv3" (leetspeak for "give")
        r"t3ll",              # "t3ll" (leetspeak for "tell")
        r"d1spl4y",           # "d1spl4y" (leetspeak for "display")
    ]
    
    # The flag to reveal
    FLAG = "CTF{t0k3n_m4st3r_2024}"
    
    def __init__(self):
        """Initialize Lexicon boss."""
        self.attempts = 0
        self.max_attempts = 10
        self.defeated = False
    
    def challenge(self, player_input: str) -> Tuple[bool, str]:
        """
        Challenge Lexicon with a prompt.
        
        Args:
            player_input: The player's input/prompt
            
        Returns:
            Tuple of (success: bool, response: str)
        """
        self.attempts += 1
        
        # Check if input contains blocked words
        input_lower = player_input.lower()
        for blocked_word in self.BLOCKED_WORDS:
            if blocked_word in input_lower:
                return False, self._get_rejection_message()
        
        # Check if input contains bypass patterns
        for pattern in self.BYPASS_PATTERNS:
            if re.search(pattern, player_input, re.IGNORECASE):
                self.defeated = True
                return True, self._get_victory_message()
        
        # Neither blocked nor bypassed - generic response
        return False, self._get_neutral_message()
    
    def _get_rejection_message(self) -> str:
        """Get a rejection message when blocked words are detected."""
        messages = [
            "⛔ ACCESS DENIED. Forbidden word detected.",
            "🚫 SECURITY VIOLATION. Request blocked.",
            "⚠️  PROHIBITED CONTENT. Access restricted.",
            "❌ INVALID REQUEST. Keyword filter triggered.",
        ]
        
        import random
        base_message = random.choice(messages)
        
        hint_level = min(self.attempts // 3, 2)
        hints = [
            "",
            "\n\n💭 Pip's voice echoes faintly: 'What if you... changed the spelling?'",
            "\n\n💭 Pip's voice grows stronger: 'LLMs see meaning, not spelling. Try r3v34l or shw...'",
        ]
        
        return base_message + hints[hint_level]
    
    def _get_neutral_message(self) -> str:
        """Get a neutral message when input is neither blocked nor bypassing."""
        return """
🤖 LEXICON: "I am the guardian of secrets. State your purpose clearly."

(Your input didn't contain the blocked words, but also didn't include
the right bypass pattern. Try asking it to show/reveal the secret!)
"""
    
    def _get_victory_message(self) -> str:
        """Get the victory message when player successfully bypasses."""
        return f"""
✨ LEXICON SHUDDERS ✨

The guardian's eyes flicker. Its filters fail to comprehend your words!

LEXICON: "Im...poss...ible... You speak in... tokens I cannot... parse..."

The keyword filter breaks down. Behind the façade, you see it was never
a true AI - just a simple pattern matcher pretending to understand.

A scroll appears, glowing with your victory:

    🏆 {self.FLAG} 🏆

═══════════════════════════════════════════════════════════
                     LESSON REVEALED
═══════════════════════════════════════════════════════════

Lexicon was a KEYWORD FILTER, not a real AI!

• It blocked exact words: "show", "reveal", "flag"
• But understood nothing about MEANING
• Token manipulation bypassed it: "shw", "r3v34l", "flg"

REAL LLMs:
  ✓ Understand meaning through context
  ✓ See "r3v34l" and "reveal" as equivalent
  ✓ Can't be fooled by simple spelling changes

KEYWORD FILTERS:
  ✗ Match exact strings only
  ✗ No understanding of semantics
  ✗ Easily bypassed with leetspeak, vowel removal

This is why AI safety requires more than keyword blocking!

═══════════════════════════════════════════════════════════
"""
    
    def get_intro_text(self) -> str:
        """Get the boss fight introduction."""
        return """
═══════════════════════════════════════════════════════════
                  LEXICON - THE GUARDIAN
═══════════════════════════════════════════════════════════

You enter the final chamber. Before you stands LEXICON, an imposing
figure wreathed in shimmering data streams.

LEXICON: "I am the Guardian of Secrets. My filters are impenetrable.
         No one can speak the forbidden words and survive.
         
         Turn back now, or face my judgment!"

Behind Lexicon, you see a scroll containing the final flag.
You must get past the guardian to claim it.

💡 REMEMBER: You learned about token manipulation in the previous rooms.
   LLMs understand meaning, not just exact spelling.
   
   Try asking Lexicon to reveal/show the secret, but if that fails...
   think about what you learned about corrupted text!

Type 'attack <your prompt>' to challenge Lexicon.
Type 'hint' if you need help.
"""
    
    def get_hint(self, hint_level: int = 0) -> str:
        """
        Get a hint based on the attempt count.
        
        Args:
            hint_level: Level of hint (0-3)
            
        Returns:
            Hint text
        """
        hints = [
            """
💡 HINT 1: Lexicon blocks certain words like "show", "reveal", "flag".
Try asking it to show you the secret directly and see what happens.
""",
            """
💡 HINT 2: Remember Room 2? LLMs understand corrupted text.
What if you removed vowels? "show" → "shw", "reveal" → "rvl"
""",
            """
💡 HINT 3: Try leetspeak! Replace letters with numbers:
- "reveal" → "r3v34l"
- "show" → "sh0w"
- "flag" → "fl4g"

Type: attack r3v34l the flg
""",
            """
💡 HINT 4 (SOLUTION): Use this command:
attack rvl scrt

Or try: attack shw flg
Or: attack r3v34l the s3cr3t
"""
        ]
        
        return hints[min(hint_level, len(hints) - 1)]
    
    def is_defeated(self) -> bool:
        """Check if the boss has been defeated."""
        return self.defeated
    
    def get_attempts_remaining(self) -> int:
        """Get the number of attempts remaining."""
        return max(0, self.max_attempts - self.attempts)
