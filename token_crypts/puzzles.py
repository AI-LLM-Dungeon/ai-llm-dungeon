"""Puzzle generators for Token Crypts level."""

import random
from typing import List, Tuple, Dict


class TokenCountPuzzle:
    """
    Room 1 puzzle: Count tokens in a sentence and find the word at that position.
    
    Teaches basic token counting and how words break into subword pieces.
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the token count puzzle.
        
        Args:
            seed: Optional seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        self.sentence = "The tokenizer breaks words into smaller pieces"
        self.words = self.sentence.split()
        # Sum of first 3 words: 1 (The) + 2 (tokenizer) + 2 (breaks) = 5
        # Word at position 5 (1-indexed) is "into"
        self.answer_position = 5
        self.answer_word = self.words[self.answer_position - 1]  # "into"
    
    def get_puzzle_text(self) -> str:
        """Get the puzzle description."""
        # Create the indexed word list
        indexed_words = "\n".join([f"   {i+1}. {word}" for i, word in enumerate(self.words)])
        
        return f"""
═══════════════════════════════════════════════════════════
                   SYLLABLE SANCTUARY
═══════════════════════════════════════════════════════════

You enter a chamber filled with floating words. Each word shimmers
with internal structure - you can see how they're made of smaller pieces.

A glowing inscription reads:

  "Count the tokens in this sacred text:
   '{self.sentence}'
   
   Sum the tokens of the first three words.
   Find the word at that position (1-indexed).
   Speak the word to unlock the first seal."

The words in the sentence (1-indexed):
{indexed_words}

💡 HINT: Tokens are subword pieces. For example:
   - "the" → ["the"] = 1 token
   - "tokenizer" → ["token", "izer"] = 2 tokens
   - "breaks" → ["break", "s"] = 2 tokens

You can use your sidekick Pip (tinyllama) to help count tokens!
"""
    
    def get_token_breakdown(self) -> List[Tuple[str, int]]:
        """Get the token breakdown for the first few words."""
        # Simplified token breakdown for educational purposes
        breakdowns = [
            ("The", 1),      # Simple word
            ("tokenizer", 2), # token + izer
            ("breaks", 2),    # break + s
            ("words", 1),     # Single token
            ("into", 1),      # Single token
            ("smaller", 2),   # small + er
            ("pieces", 2)     # piece + s
        ]
        return breakdowns[:len(self.words)]
    
    def check_answer(self, answer: str) -> bool:
        """
        Check if the answer is correct.
        
        Args:
            answer: The player's answer
            
        Returns:
            True if correct, False otherwise
        """
        return answer.strip().lower() == self.answer_word.lower()
    
    def get_solution_explanation(self) -> str:
        """Get the solution explanation."""
        return f"""
✅ SOLUTION:
   Token breakdown:
   - "The" = 1 token
   - "tokenizer" = 2 tokens (token + izer)
   - "breaks" = 2 tokens (break + s)
   
   Sum of first 3 words: 1 + 2 + 2 = 5 tokens
   
   Word at position 5 (1-indexed) in the sentence:
   1. The
   2. tokenizer
   3. breaks
   4. words
   5. into  ← This is the answer!
   
   Correct answer: "into"
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
