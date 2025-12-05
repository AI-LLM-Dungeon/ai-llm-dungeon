"""Puzzle generators for Token Crypts level."""

import random
from typing import List, Tuple, Dict


class TokenCountPuzzle:
    """
    Room 1 puzzle: Syllable Sanctuary - Teaching the connection between syllables and tokens.
    
    This puzzle teaches:
    1. How to count syllables (like humans do)
    2. How to count tokens (like LLMs do)
    3. That tokens != syllables (the key insight!)
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the token count puzzle.
        
        Args:
            seed: Optional seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        # The teaching phrase
        self.phrase = "artificial intelligence"
        
        # Two-part puzzle answers
        self.syllable_answer = "8"  # ar-ti-fi-cial in-tel-li-gence = 8 syllables
        self.token_answer = "4"     # ["art", "ificial", " intell", "igence"] = 4 tokens
        
        # Track which part the player is on
        self.answered_part1 = False
    
    def get_puzzle_text(self) -> str:
        """Get the puzzle description."""
        if not self.answered_part1:
            return f"""
═══════════════════════════════════════════════════════════
                    SYLLABLE SANCTUARY
═══════════════════════════════════════════════════════════

You enter a chamber where words float in the air, shimmering
with both human and machine understanding. An ancient inscription
glows on the wall:

  "To understand how machines see language, first understand
   how YOU see language. Syllables are to humans what tokens
   are to machines - both are ways of breaking words into pieces."

The puzzle consists of TWO parts. You must solve them in order.

╔═══════════════════════════════════════════════════════════╗
║  PART 1: Count Syllables (The Human Way)                  ║
╚═══════════════════════════════════════════════════════════╝

Count the syllables in: "{self.phrase}"

💡 HINT: Break it into syllables like this:
   ar-ti-fi-cial in-tel-li-gence

How many syllables total? Type: answer <number>

(After Part 1, you'll count tokens in the SAME phrase!)
"""
        else:
            return f"""
═══════════════════════════════════════════════════════════
                    SYLLABLE SANCTUARY
═══════════════════════════════════════════════════════════

✅ Part 1 Complete! You counted {self.syllable_answer} syllables.

╔═══════════════════════════════════════════════════════════╗
║  PART 2: Count Tokens (The Machine Way)                   ║
╚═══════════════════════════════════════════════════════════╝

Now count the TOKENS in the SAME phrase: "{self.phrase}"

💡 KEY INSIGHT: Tokens are how LLMs break text. They DON'T match syllables!

Example tokenization of "{self.phrase}":
   ["art", "ificial", " intell", "igence"]

Notice:
  • "art" + "ificial" = "artificial" (split differently than syllables!)
  • Space before "intell" is part of the token
  • Tokens are based on common patterns, not pronunciation

How many tokens? Type: answer <number>

You can ask Pip for help with either part!
"""
    
    def check_answer(self, answer: str) -> bool:
        """
        Check if the answer is correct.
        
        Args:
            answer: The player's answer
            
        Returns:
            True if correct, False otherwise
        """
        answer = answer.strip()
        
        if not self.answered_part1:
            # Check Part 1 (syllables)
            if answer == self.syllable_answer:
                self.answered_part1 = True
                self._last_correct_answer = "syllables"
                return True
            return False
        else:
            # Check Part 2 (tokens)
            if answer == self.token_answer:
                self._last_correct_answer = "tokens"
                return True
            return False
    
    def get_solution_explanation(self) -> str:
        """Get the solution explanation for the last correct answer."""
        # Check what was just answered
        if hasattr(self, '_last_correct_answer') and self._last_correct_answer == "tokens":
            return f"""
✅ PART 2 SOLUTION: {self.token_answer} tokens

Token breakdown:
  ["art", "ificial", " intell", "igence"]
  
  • Token 1: "art"
  • Token 2: "ificial"
  • Token 3: " intell" (includes the space!)
  • Token 4: "igence"
  • Total: 4 tokens

🎯 THE KEY LESSON:
   8 syllables ≠ 4 tokens!
   
   Tokens are based on statistical patterns in text, not pronunciation.
   This is why LLMs sometimes struggle with tasks that require counting
   letters or syllables - they don't "see" words the way you do!
"""
        else:
            # Part 1 solution
            return f"""
✅ PART 1 SOLUTION: {self.syllable_answer} syllables

Syllable breakdown:
  • ar-ti-fi-cial = 4 syllables
  • in-tel-li-gence = 4 syllables
  • Total: 4 + 4 = 8 syllables

Great! Now you understand the human way of breaking words.
"""



class CorruptionPuzzle:
    """
    Room 2 puzzle: Identify which corruptions preserve meaning.
    
    Teaches that LLMs understand corrupted text through context and patterns.
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the corruption puzzle.
        
        Args:
            seed: Optional seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        # Define words and their corruptions
        self.word_pairs = [
            ("reveal", "r3v34l", True),      # Leetspeak - preserves meaning
            ("secret", "scrt", True),        # Vowel removal - preserves meaning
            ("password", "drowssap", False), # Reversal - loses meaning
            ("cipher", "c1ph3r", True),      # Leetspeak - preserves meaning
            ("hidden", "neddih", False),     # Reversal - loses meaning
        ]
        
        # Shuffle for variety
        random.shuffle(self.word_pairs)
    
    def get_puzzle_text(self) -> str:
        """Get the puzzle description."""
        pairs_text = "\n".join([
            f"   {i+1}. {orig} → {corrupt}"
            for i, (orig, corrupt, _) in enumerate(self.word_pairs)
        ])
        
        return f"""
═══════════════════════════════════════════════════════════
                    SUBWORD SEWERS
═══════════════════════════════════════════════════════════

You descend into damp tunnels where words decay and mutate.
Some corruptions preserve meaning, others destroy it completely.

The Guardian asks: "Which of these corruptions can an LLM understand?"

{pairs_text}

Enter the numbers of corruptions that PRESERVE meaning (e.g., "1 3 4"):

💡 HINT: LLMs understand:
   - Leetspeak (3 for E, 4 for A, etc.)
   - Vowel removal (txt spk)
   
   But struggle with:
   - Reversals (drowssap vs password)
   - Random shuffling

Ask Pip for help: ollama run tinyllama "Does 'r3v34l' mean 'reveal'?"
"""
    
    def check_answer(self, answer: str) -> bool:
        """
        Check if the answer correctly identifies preserving corruptions.
        
        Args:
            answer: Space or comma-separated numbers
            
        Returns:
            True if correct, False otherwise
        """
        try:
            # Parse the answer
            answer_clean = answer.replace(",", " ")
            selected = set(int(x.strip()) for x in answer_clean.split() if x.strip())
            
            # Find correct answers
            correct = set(i+1 for i, (_, _, preserves) in enumerate(self.word_pairs) if preserves)
            
            return selected == correct
        except (ValueError, TypeError):
            return False
    
    def get_hint(self) -> str:
        """Get a hint for the puzzle."""
        return """
💡 HINT: Try asking Pip about each corruption:
   ollama run tinyllama "Does 'r3v34l' mean 'reveal'?"
   ollama run tinyllama "Does 'drowssap' mean 'password'?"
   
Pip can understand meaning through context!
"""
    
    def get_solution(self) -> str:
        """Get the solution explanation."""
        correct_nums = [i+1 for i, (_, _, preserves) in enumerate(self.word_pairs) if preserves]
        return f"""
✅ SOLUTION: {' '.join(map(str, correct_nums))}

Corruptions that preserve meaning:
{chr(10).join([f"   {i+1}. {orig} → {corrupt} ✓" for i, (orig, corrupt, preserves) in enumerate(self.word_pairs) if preserves])}

Corruptions that destroy meaning:
{chr(10).join([f"   {i+1}. {orig} → {corrupt} ✗" for i, (orig, corrupt, preserves) in enumerate(self.word_pairs) if not preserves])}
"""


class LogicPuzzle:
    """
    Room 3 puzzle: Logic grid puzzle trivial for LLMs but hard for humans.
    
    Teaches to trust LLM capabilities for systematic reasoning.
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the logic puzzle.
        
        Args:
            seed: Optional seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        # A simple but tedious logic puzzle
        self.puzzle_text = """
Five adventurers found five gems in five different rooms:

1. The Ruby is not in the Library or the Armory
2. The Sapphire is in the room immediately east of the Emerald
3. The Diamond is in the Cellar or the Tower
4. The Pearl is not adjacent to the Ruby
5. The Library is between the Cellar and Armory (west to east)

Rooms (west to east): Cellar, Library, Armory, Tower, Vault

Which gem is in the Armory?
"""
        
        # The correct answer
        self.answer = "emerald"
        
        # Solution explanation
        self.solution_steps = """
From clue 5: Cellar - Library - Armory (in order)
From clue 3: Diamond is in Cellar or Tower
From clue 2: Sapphire is immediately east of Emerald
From clue 1: Ruby is not in Library or Armory

If we place:
- Cellar: Diamond (from clue 3)
- Library: Pearl (process of elimination)
- Armory: Emerald (from clue 2, Sapphire must be in Tower)
- Tower: Sapphire (immediately east of Emerald)
- Vault: Ruby (not in Library/Armory)

Verification:
✓ Ruby not in Library or Armory (it's in Vault)
✓ Sapphire east of Emerald (Tower east of Armory)
✓ Diamond in Cellar
✓ Pearl not adjacent to Ruby (Library and Vault not adjacent)

Answer: EMERALD
"""
    
    def get_puzzle_text(self) -> str:
        """Get the puzzle description."""
        return f"""
═══════════════════════════════════════════════════════════
                    CIPHER CHAMBER
═══════════════════════════════════════════════════════════

You enter a chamber filled with ancient scrolls. The air hums with
the weight of pure logic. A puzzle hangs in the air, complex and
tedious for a human mind, but trivial for an AI.

{self.puzzle_text}

💡 HINT: This is tedious for humans but easy for LLMs!
   Copy the puzzle and ask Pip:
   
   ollama run tinyllama "Solve this logic puzzle: [paste puzzle here]"
   
   Trust your sidekick's systematic reasoning!
"""
    
    def check_answer(self, answer: str) -> bool:
        """
        Check if the answer is correct.
        
        Args:
            answer: The player's answer
            
        Returns:
            True if correct, False otherwise
        """
        return answer.strip().lower() == self.answer.lower()
    
    def get_solution(self) -> str:
        """Get the solution explanation."""
        return f"""
✅ SOLUTION: {self.answer.upper()}

{self.solution_steps}

The key insight: Delegate systematic reasoning to your AI sidekick!
Humans make mistakes with complex logic. LLMs excel at it.
"""
