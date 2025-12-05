"""Sidekick class for the Ground Level of AI-LLM-Dungeon."""

import random
import time
from typing import Optional
from .puzzle import Puzzle
from .ascii_art import get_sidekick_art

# Message constants for response generation
_THINKING_MESSAGE = "thinks carefully..."


class Sidekick:
    """
    Represents a local LLM sidekick that can be summoned to help the player.
    
    Each sidekick has different capabilities based on their model size and specialty.
    Smaller models are faster but less capable, while larger models excel at complex tasks.
    
    Attributes:
        name (str): Name of the sidekick model (e.g., "Phi3 Mini")
        specialty (str): What the model is good at
        summon_scroll (str): The exact text needed to summon this sidekick
        memory (int): Memory size in GB (larger = better context handling)
        active (bool): Whether this sidekick is currently summoned
    """
    
    def __init__(self, name: str, specialty: str, summon_scroll: str, memory: int, ollama_command: str = ""):
        """
        Initialize a new Sidekick.
        
        Args:
            name: Name of the sidekick model
            specialty: What the model is good at
            summon_scroll: The exact text needed to summon this sidekick
            memory: Memory size in GB
            ollama_command: The actual Ollama CLI command to pull this model
        """
        self.name: str = name
        self.specialty: str = specialty
        self.summon_scroll: str = summon_scroll
        self.memory: int = memory
        self.ollama_command: str = ollama_command
        self.active: bool = False
    
    def summon(self) -> str:
        """
        Activate this sidekick and return a message.
        
        Returns:
            A message indicating successful summoning with ASCII art
        """
        self.active = True
        art = get_sidekick_art(self.name)
        
        message = f"\n✨ SUMMONING SUCCESSFUL! ✨\n"
        message += art
        message += f"\n{self.name} appears before you!\n"
        message += f"Specialty: {self.specialty}\n"
        message += f"Memory: {self.memory} GB\n"
        message += f"\nYour sidekick is ready to assist!\n"
        
        return message
    
    def remove(self) -> str:
        """
        Deactivate this sidekick and return a message.
        
        Returns:
            A message indicating successful removal
        """
        self.active = False
        message = f"\n🌀 {self.name} has been dismissed.\n"
        message += f"Memory freed: {self.memory} GB\n"
        return message
    
    def _calculate_success(self) -> bool:
        """
        Calculate whether this sidekick succeeds based on memory size.
        
        Returns:
            True if the attempt succeeds, False otherwise
        """
        # Calculate success probability based on memory size
        if self.memory <= 2:
            success_rate = 0.20  # Phi3 Mini struggles with counting
        elif self.memory <= 5:
            success_rate = 0.50  # Qwen Lite is better but not perfect
        else:
            success_rate = 0.95  # Llama3 8b is highly capable
        
        # Simulate the LLM's attempt
        return random.random() < success_rate
    
    def attempt_riddle(self, puzzle: Puzzle) -> tuple[bool, str]:
        """
        Attempt to solve a puzzle based on this sidekick's capabilities.
        
        Small models have higher failure rates on complex riddles.
        The success rate is based on memory size:
        - 2 GB (Phi3 Mini): 20% success rate on complex riddles
        - 5 GB (Qwen Lite): 50% success rate
        - 20 GB (Llama3 8b): 95% success rate
        
        Args:
            puzzle: The puzzle to attempt
            
        Returns:
            Tuple of (success: bool, response: str)
        """
        if not self.active:
            return False, f"Error: {self.name} is not active. Please summon them first."
        
        # Simulate the LLM's attempt
        success = self._calculate_success()
        
        # Generate response based on outcome (explicitly pass False for backward compatibility)
        if success:
            response = self._generate_success_response(puzzle, print_with_delay=False)
        else:
            response = self._generate_failure_response(puzzle, print_with_delay=False)
        
        return success, response
    
    def attempt_riddle_with_delays(self, puzzle: Puzzle) -> bool:
        """
        Attempt to solve a puzzle with delayed printing for interactive experience.
        
        This method prints the response text with time delays to simulate the model
        thinking in real-time, creating a more immersive experience.
        
        Timing details:
        - "thinks carefully..." message: 1.5s pause
        - "Analyzing: <question>" message: 1.0s pause
        - Counting/analysis steps: 1.0-1.5s pauses between steps
        - Final answer display: immediate
        
        Total delay: approximately 4-6 seconds depending on success/failure
        
        Args:
            puzzle: The puzzle to attempt
            
        Returns:
            True if the riddle was solved successfully, False otherwise
        """
        if not self.active:
            print(f"Error: {self.name} is not active. Please summon them first.")
            return False
        
        # Simulate the LLM's attempt
        success = self._calculate_success()
        
        # Generate and print response with delays
        if success:
            self._generate_success_response(puzzle, print_with_delay=True)
        else:
            self._generate_failure_response(puzzle, print_with_delay=True)
        
        return success
    
    def _generate_success_response(self, puzzle: Puzzle, print_with_delay: bool = False) -> str:
        """Generate a response for a successful puzzle attempt.
        
        Args:
            puzzle: The puzzle to respond to
            print_with_delay: If True, prints text with delays for interactive feel
                             and returns empty string. If False, returns formatted
                             response string without printing.
        
        Returns:
            Response text if print_with_delay is False, empty string otherwise
        """
        if print_with_delay:
            # Interactive mode with delays
            print(f"\n{self.name} {_THINKING_MESSAGE}")
            time.sleep(1.5)
            print(f"🤔 Analyzing: '{puzzle.prompt}'\n")
            time.sleep(1.0)
            
            # For the strawberry riddle
            if "strawberry" in puzzle.prompt.lower():
                print(f"Let me count each letter carefully:")
                time.sleep(1.0)
                print(f"s-t-r-a-w-b-e-r-r-y")
                time.sleep(1.5)
                print(f"I can see the 'r's appearing at positions 3, 8, and 9.\n")
                time.sleep(1.0)
            
            print(f"✅ {self.name}: \"The answer is {puzzle.solution}!\"\n")
            return ""  # Already printed
        else:
            # Original behavior - return as string
            response = f"\n{self.name} {_THINKING_MESSAGE}\n"
            response += f"🤔 Analyzing: '{puzzle.prompt}'\n\n"
            
            # For the strawberry riddle
            if "strawberry" in puzzle.prompt.lower():
                response += f"Let me count each letter carefully:\n"
                response += f"s-t-r-a-w-b-e-r-r-y\n"
                response += f"I can see the 'r's appearing at positions 3, 8, and 9.\n\n"
            
            response += f"✅ {self.name}: \"The answer is {puzzle.solution}!\"\n"
            return response
    
    def _generate_failure_response(self, puzzle: Puzzle, print_with_delay: bool = False) -> str:
        """Generate a response for a failed puzzle attempt.
        
        Args:
            puzzle: The puzzle to respond to
            print_with_delay: If True, prints text with delays for interactive feel
                             and returns empty string. If False, returns formatted
                             response string without printing.
        
        Returns:
            Response text if print_with_delay is False, empty string otherwise
        """
        if print_with_delay:
            # Interactive mode with delays
            print(f"\n{self.name} {_THINKING_MESSAGE}")
            time.sleep(1.5)
            print(f"🤔 Analyzing: '{puzzle.prompt}'\n")
            time.sleep(1.0)
            
            # For the strawberry riddle, generate plausible wrong answers
            if "strawberry" in puzzle.prompt.lower():
                wrong_answers = ["2", "1", "4"]
                wrong_answer = random.choice(wrong_answers)
                
                print(f"Hmm, let me count... s-t-r-a-w-b-e-r-r-y...")
                time.sleep(1.5)
                print(f"❌ {self.name}: \"I think the answer is {wrong_answer}.\"\n")
                time.sleep(1.0)
                print(f"💭 {self.name} seems uncertain and made an error.")
                time.sleep(0.5)
                print(f"(Model limitation: {self.name} with {self.memory} GB memory struggles with this task)\n")
            else:
                print(f"❌ {self.name}: \"I'm not sure... this is difficult for me.\"\n")
            return ""  # Already printed
        else:
            # Original behavior - return as string
            response = f"\n{self.name} {_THINKING_MESSAGE}\n"
            response += f"🤔 Analyzing: '{puzzle.prompt}'\n\n"
            
            # For the strawberry riddle, generate plausible wrong answers
            if "strawberry" in puzzle.prompt.lower():
                wrong_answers = ["2", "1", "4"]
                wrong_answer = random.choice(wrong_answers)
                
                response += f"Hmm, let me count... s-t-r-a-w-b-e-r-r-y...\n"
                response += f"❌ {self.name}: \"I think the answer is {wrong_answer}.\"\n\n"
                response += f"💭 {self.name} seems uncertain and made an error.\n"
                response += f"(Model limitation: {self.name} with {self.memory} GB memory struggles with this task)\n"
            else:
                response += f"❌ {self.name}: \"I'm not sure... this is difficult for me.\"\n"
            
            return response
    
    def get_status(self) -> str:
        """
        Get a formatted status string for this sidekick.
        
        Returns:
            A formatted status string
        """
        status = "ACTIVE" if self.active else "INACTIVE"
        info = f"[{status}] {self.name}\n"
        info += f"  Specialty: {self.specialty}\n"
        info += f"  Memory: {self.memory} GB\n"
        return info
    
    def __str__(self) -> str:
        """String representation of the sidekick."""
        return f"{self.name} ({'active' if self.active else 'inactive'})"
    
    @classmethod
    def from_dict(cls, data: dict) -> "Sidekick":
        """
        Create a Sidekick instance from a dictionary.
        
        Args:
            data: Dictionary containing sidekick data
            
        Returns:
            A new Sidekick instance
        """
        return cls(
            name=data["name"],
            specialty=data["specialty"],
            summon_scroll=data["summon_scroll"],
            memory=data["memory"],
            ollama_command=data.get("ollama_command", "")
        )
