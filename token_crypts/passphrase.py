"""Dynamic passphrase generation for Token Crypts level."""

import random
from typing import List, Tuple


class PassphraseGenerator:
    """
    Generates unique 3-word passphrases for each playthrough.
    
    Uses word pools categorized by difficulty to ensure fair challenge
    and prevent memorization across multiple playthroughs.
    """
    
    # Word pools for different difficulty levels
    EASY_WORDS = [
        "ancient", "bright", "crystal", "divine", "eternal",
        "golden", "hidden", "mystic", "sacred", "silver"
    ]
    
    MEDIUM_WORDS = [
        "cipher", "enigma", "matrix", "nexus", "oracle",
        "phantom", "quantum", "riddle", "shadow", "wisdom"
    ]
    
    HARD_WORDS = [
        "algorithm", "byzantine", "cryptograph", "ephemeral", "labyrinth",
        "metamorphic", "paradox", "synthesis", "transcend", "zenith"
    ]
    
    def __init__(self, seed: int = None):
        """
        Initialize the passphrase generator.
        
        Args:
            seed: Optional seed for reproducibility. If None, uses random seed.
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self._passphrase: List[str] = []
        self._generate()
    
    def _generate(self) -> None:
        """Generate a new 3-word passphrase from the word pools."""
        word1 = random.choice(self.EASY_WORDS)
        word2 = random.choice(self.MEDIUM_WORDS)
        word3 = random.choice(self.HARD_WORDS)
        self._passphrase = [word1, word2, word3]
    
    def get_word(self, position: int) -> str:
        """
        Get the passphrase word at the specified position (1-3).
        
        Args:
            position: Position of the word (1, 2, or 3)
            
        Returns:
            The word at that position
            
        Raises:
            ValueError: If position is not 1, 2, or 3
        """
        if position < 1 or position > 3:
            raise ValueError("Position must be 1, 2, or 3")
        return self._passphrase[position - 1]
    
    def get_full_passphrase(self) -> str:
        """
        Get the complete passphrase as a space-separated string.
        
        Returns:
            The full passphrase (e.g., "ancient cipher algorithm")
        """
        return " ".join(self._passphrase)
    
    def check_passphrase(self, attempt: str) -> bool:
        """
        Check if the attempted passphrase matches the correct one.
        
        Args:
            attempt: The passphrase attempt (case-insensitive)
            
        Returns:
            True if correct, False otherwise
        """
        return attempt.strip().lower() == self.get_full_passphrase().lower()
    
    @staticmethod
    def get_token_breakdown(word: str) -> List[str]:
        """
        Simulate a simple token breakdown for educational purposes.
        
        This is a simplified approximation of how LLMs tokenize words.
        Real tokenizers are more complex (BPE, WordPiece, etc.).
        
        Args:
            word: The word to break down
            
        Returns:
            List of token-like subword pieces
        """
        # Simple heuristic: break on syllable boundaries
        tokens = []
        word_lower = word.lower()
        
        # Common prefixes
        prefixes = ['un', 're', 'pre', 'post', 'anti', 'de', 'dis', 'mis', 'over', 'sub']
        for prefix in prefixes:
            if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 2:
                tokens.append(prefix)
                word_lower = word_lower[len(prefix):]
                break
        
        # Common suffixes
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful']
        suffix_found = None
        for suffix in suffixes:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                suffix_found = suffix
                word_lower = word_lower[:-len(suffix)]
                break
        
        # Break remaining word into syllable-like chunks (simplified)
        if len(word_lower) <= 4:
            tokens.append(word_lower)
        else:
            # Split roughly in middle for demonstration
            mid = len(word_lower) // 2
            tokens.append(word_lower[:mid])
            tokens.append(word_lower[mid:])
        
        if suffix_found:
            tokens.append(suffix_found)
        
        return tokens
    
    def get_token_count(self, word: str) -> int:
        """
        Get the approximate token count for a word.
        
        Args:
            word: The word to count tokens for
            
        Returns:
            Number of tokens (subword pieces)
        """
        return len(self.get_token_breakdown(word))
