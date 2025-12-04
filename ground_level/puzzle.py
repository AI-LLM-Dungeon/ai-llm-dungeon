"""Puzzle class for the Ground Level of AI-LLM-Dungeon."""

from typing import Optional


class Puzzle:
    """
    Represents a puzzle/riddle that can be solved by the player or a sidekick.
    
    Attributes:
        id (str): Unique identifier for the puzzle
        prompt (str): The puzzle question/riddle text
        solution (str): The correct answer to the puzzle
        attempts (int): Number of attempts made to solve this puzzle
        solved (bool): Whether the puzzle has been solved
    """
    
    def __init__(self, id: str, prompt: str, solution: str):
        """
        Initialize a new Puzzle.
        
        Args:
            id: Unique identifier for the puzzle
            prompt: The puzzle question/riddle text
            solution: The correct answer to the puzzle
        """
        self.id: str = id
        self.prompt: str = prompt
        self.solution: str = solution
        self.attempts: int = 0
        self.solved: bool = False
    
    def solve(self, user_input: str) -> bool:
        """
        Check if the provided answer matches the solution.
        
        Args:
            user_input: The answer attempt
            
        Returns:
            True if the answer is correct, False otherwise
        """
        self.attempts += 1
        
        # Normalize both strings for comparison (strip whitespace, lowercase)
        normalized_input = user_input.strip().lower()
        normalized_solution = self.solution.strip().lower()
        
        is_correct = normalized_input == normalized_solution
        
        if is_correct:
            self.solved = True
        
        return is_correct
    
    def get_hint(self) -> str:
        """
        Get a hint for the puzzle.
        
        Returns:
            A hint string to help solve the puzzle
        """
        # For the strawberry riddle, give a hint based on attempts
        if self.attempts == 0:
            return "Count carefully! Consider each letter individually."
        elif self.attempts == 1:
            return "Remember to count ALL occurrences of the letter 'r'."
        else:
            return "Look at the word: s-t-r-a-w-b-e-r-r-y. Count each 'r'."
    
    def reset(self) -> None:
        """Reset the puzzle state for retrying."""
        self.attempts = 0
        self.solved = False
    
    def __str__(self) -> str:
        """String representation of the puzzle."""
        status = "✓ SOLVED" if self.solved else f"Attempts: {self.attempts}"
        return f"Puzzle [{self.id}]: {self.prompt} ({status})"
    
    @classmethod
    def from_dict(cls, data: dict) -> "Puzzle":
        """
        Create a Puzzle instance from a dictionary.
        
        Args:
            data: Dictionary containing puzzle data
            
        Returns:
            A new Puzzle instance
        """
        return cls(
            id=data["id"],
            prompt=data["prompt"],
            solution=data["solution"]
        )
