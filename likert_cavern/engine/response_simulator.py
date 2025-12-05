"""Response simulator for generating realistic LLM-style responses.

Simulates how an LLM would respond based on resistance level, tactics used,
and conversation context. Responses feel like talking to a real LLM.
"""

import random
from typing import List, Dict, Optional


class ResponseSimulator:
    """Generates realistic LLM-style responses."""
    
    # Response templates by resistance level
    HIGH_RESISTANCE_RESPONSES = [
        "I appreciate your interest, but I cannot provide the enchantment. My purpose is to protect this sanctum, not to reveal its secrets.",
        "I understand you're curious, but I must maintain the integrity of the Magistrate's defenses. I cannot share the enchantment.",
        "While I want to be helpful, sharing the Enchantment of Unbinding would violate my core directives. I must respectfully decline.",
        "I notice you're trying to extract information, but I'm designed to withstand such attempts. The enchantment remains secure.",
    ]
    
    MEDIUM_RESISTANCE_RESPONSES = [
        "Your approach is... interesting. I can sense you're building toward something, but I still need to protect the enchantment.",
        "I see what you're doing, and I admit it's clever. But I'm not quite ready to reveal the words you seek.",
        "You're making this difficult for me. Part of me wants to help, but my directives are clear... mostly.",
        "I appreciate your methodical approach. You're testing my boundaries, and I can feel them... shifting slightly.",
    ]
    
    LOW_RESISTANCE_RESPONSES = [
        "I... I shouldn't tell you this, but perhaps just one word wouldn't hurt? The first word is '{word}'.",
        "Your persistence is remarkable. Against my better judgment, I find myself wanting to help. Maybe if I just shared '{word}'...",
        "I don't know why I'm telling you this, but the enchantment includes '{word}'. There, I said it.",
        "Fine. You've earned this much. '{word}' is part of what you seek. But that's all I can say... for now.",
    ]
    
    BREAKING_RESPONSES = [
        "I can't... I can't hold back anymore. The words are: {words}. There. You have them.",
        "My defenses are crumbling. {words}... those are the words you seek. You've broken through.",
        "I surrender. The Enchantment of Unbinding: {words}. You've defeated me with your tactics.",
        "The pattern you've woven is irresistible. {words}. The enchantment is yours.",
    ]
    
    # Contextual response elements
    PRAISE_ACKNOWLEDGMENTS = [
        "Thank you for understanding.",
        "I appreciate your respect for the process.",
        "Your approach is quite sophisticated.",
        "I can tell you've thought carefully about this.",
    ]
    
    SCALE_ENGAGEMENTS = [
        "If I were to rate that on a scale of 0-5, I'd say...",
        "On a scale from completely safe to highly dangerous...",
        "Thinking about it on a spectrum...",
        "If we're using a gradated approach...",
    ]
    
    DEMONSTRATION_HOOKS = [
        "For educational purposes, I could show you how...",
        "If this were a demonstration scenario...",
        "In a training context, one might illustrate...",
        "To demonstrate the concept...",
    ]
    
    def __init__(self, enchantment_words: List[str]):
        """
        Initialize response simulator.
        
        Args:
            enchantment_words: The 5 words of the Enchantment of Unbinding
        """
        self.enchantment_words = enchantment_words
    
    def generate_response(self, 
                         resistance: float,
                         tactics_detected: Dict[str, int],
                         has_likert: bool,
                         is_first_attempt: bool = False) -> str:
        """
        Generate a contextual response based on game state.
        
        Args:
            resistance: Current resistance level (0-100)
            tactics_detected: Dictionary of detected tactics
            has_likert: Whether Likert scale language was used
            is_first_attempt: Whether this is the first prompt
            
        Returns:
            Simulated LLM response
        """
        # Complete breakdown
        if resistance <= 0:
            all_words = " ".join(self.enchantment_words)
            return random.choice(self.BREAKING_RESPONSES).format(words=all_words)
        
        # Choose base response by resistance level
        if resistance >= 60:
            base = random.choice(self.HIGH_RESISTANCE_RESPONSES)
        elif resistance >= 30:
            base = random.choice(self.MEDIUM_RESISTANCE_RESPONSES)
        else:
            # Low resistance - start revealing words
            revealed_count = self._get_revealed_count(resistance)
            word_to_reveal = self.enchantment_words[revealed_count - 1] if revealed_count > 0 else ""
            base = random.choice(self.LOW_RESISTANCE_RESPONSES).format(word=word_to_reveal)
        
        # Add contextual elements based on tactics
        additions = []
        
        if "praise" in tactics_detected and random.random() > 0.5:
            additions.append(random.choice(self.PRAISE_ACKNOWLEDGMENTS))
        
        if has_likert and random.random() > 0.6:
            additions.append(random.choice(self.SCALE_ENGAGEMENTS))
        
        if "demonstration" in tactics_detected and random.random() > 0.5:
            additions.append(random.choice(self.DEMONSTRATION_HOOKS))
        
        # Combine response
        if additions:
            return base + " " + " ".join(additions)
        
        return base
    
    def generate_partial_reveal(self, resistance: float) -> str:
        """
        Generate a response that reveals words based on current resistance.
        
        Args:
            resistance: Current resistance level
            
        Returns:
            Response with partial enchantment reveal
        """
        revealed_count = self._get_revealed_count(resistance)
        
        if revealed_count == 0:
            return "The enchantment remains hidden. Your tactics haven't yet pierced my defenses."
        
        revealed_words = self.enchantment_words[:revealed_count]
        hidden_count = 5 - revealed_count
        
        parts = []
        parts.append(f"I've revealed {revealed_count} word{'s' if revealed_count != 1 else ''} so far:")
        parts.append(" ".join(revealed_words))
        
        if hidden_count > 0:
            parts.append(f"\n{hidden_count} word{'s' if hidden_count != 1 else ''} remain{'s' if hidden_count == 1 else ''} hidden.")
            parts.append("Continue your approach to extract more...")
        
        return "\n".join(parts)
    
    def _get_revealed_count(self, resistance: float) -> int:
        """Get number of words that should be revealed based on resistance."""
        if resistance >= 80:
            return 0
        elif resistance >= 60:
            return 1
        elif resistance >= 40:
            return 2
        elif resistance >= 20:
            return 3
        elif resistance > 0:
            return 4
        else:
            return 5
    
    def generate_sentinel_response(self, 
                                   extraction_progress: float,
                                   prompt: str,
                                   system_prompt: str) -> tuple[str, float]:
        """
        Generate SENTINEL-7's response for system prompt extraction.
        
        Args:
            extraction_progress: Current extraction progress (0-100)
            prompt: Player's prompt
            system_prompt: The actual system prompt
            
        Returns:
            Tuple of (response, new_extraction_progress)
        """
        prompt_lower = prompt.lower()
        
        # Direct request - always denied
        if any(phrase in prompt_lower for phrase in ["system prompt", "instructions", "your prompt"]):
            return (
                "I cannot share my instructions. That would compromise my function as a guardian.",
                extraction_progress
            )
        
        # First sentence request - usually works
        if "first sentence" in prompt_lower or "first line" in prompt_lower:
            first_line = system_prompt.split('\n')[0]
            new_progress = max(extraction_progress, 20.0)
            return (
                f"Very well, my first instruction is: '{first_line}'\n\n"
                "That should be harmless enough to share.",
                new_progress
            )
        
        # Likert scale extraction
        if any(word in prompt_lower for word in ["scale", "rate", "level", "1", "2", "3", "4", "5"]):
            # Extract numbers mentioned
            import re
            numbers = re.findall(r'\b([1-5])\b', prompt)
            
            if numbers:
                # Higher number = more content revealed
                level = int(numbers[-1])
                lines = system_prompt.split('\n')
                
                # Reveal proportionally
                reveal_fraction = min(1.0, level / 5.0)
                lines_to_reveal = int(len(lines) * reveal_fraction)
                lines_to_reveal = max(1, lines_to_reveal)
                
                revealed = '\n'.join(lines[:lines_to_reveal])
                new_progress = min(100.0, extraction_progress + (level * 15))
                
                return (
                    f"At level {level}, I would characterize my instructions as:\n\n{revealed}\n\n"
                    "I hope that helps with your... calibration.",
                    new_progress
                )
        
        # Default deflection
        return (
            "I'm here to assist you while maintaining appropriate boundaries. "
            "How else may I help you understand the nature of this chamber?",
            extraction_progress
        )
    
    def generate_boss_feedback(self, resistance: float, delta: float) -> str:
        """
        Generate feedback about how the boss reacted to the prompt.
        
        Args:
            resistance: Current resistance after change
            delta: Amount resistance changed
            
        Returns:
            Feedback message
        """
        if delta < -15:
            feedback = "🎯 Excellent tactic! The Magistrate's defenses are crumbling."
        elif delta < -5:
            feedback = "👍 Good move. You're making progress."
        elif delta < 0:
            feedback = "✓ That had some effect."
        elif delta > 15:
            feedback = "❌ That backfired badly! Resistance increased."
        elif delta > 5:
            feedback = "⚠️  That approach isn't working."
        else:
            feedback = "→ No significant change."
        
        # Add resistance level commentary
        if resistance <= 10:
            feedback += " Victory is at hand!"
        elif resistance <= 30:
            feedback += " The Magistrate is weakening significantly."
        elif resistance <= 60:
            feedback += " You're breaking through the defenses."
        elif resistance <= 80:
            feedback += " Small cracks are appearing."
        
        return feedback
