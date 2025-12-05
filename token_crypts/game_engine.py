"""Game engine for Token Crypts level."""

from enum import Enum
from typing import Optional, Dict, Any
from .passphrase import PassphraseGenerator
from .puzzles import TokenCountPuzzle, CorruptionPuzzle, LogicPuzzle
from .boss import LexiconBoss


class GameState(Enum):
    """Game state enumeration."""
    INTRO = "intro"
    ROOM_1 = "room_1"
    ROOM_2 = "room_2"
    ROOM_3 = "room_3"
    SUMMONING_GATE = "summoning_gate"
    BOSS_FIGHT = "boss_fight"
    VICTORY = "victory"


class PlayerProgress:
    """Track player progress through the level."""
    
    def __init__(self):
        """Initialize player progress."""
        self.words_collected: list[str] = []
        self.rooms_completed: set[str] = set()
        self.sidekick_pulled: bool = False
        self.sidekick_released: bool = False
        self.boss_defeated: bool = False
    
    def add_word(self, word: str) -> None:
        """Add a passphrase word to the player's collection."""
        if word not in self.words_collected:
            self.words_collected.append(word)
    
    def complete_room(self, room_id: str) -> None:
        """Mark a room as completed."""
        self.rooms_completed.add(room_id)
    
    def has_completed_room(self, room_id: str) -> bool:
        """Check if a room has been completed."""
        return room_id in self.rooms_completed
    
    def get_status(self) -> str:
        """Get formatted status string."""
        return f"""
═══════════════════════════════════════════════════════════
                     PLAYER STATUS
═══════════════════════════════════════════════════════════
Passphrase Words: {len(self.words_collected)}/3
Rooms Completed: {len(self.rooms_completed)}/3
Sidekick Status: {'Pulled' if self.sidekick_pulled else 'Not pulled'}
                 {'Released' if self.sidekick_released else 'Active' if self.sidekick_pulled else 'N/A'}
Boss Status: {'Defeated' if self.boss_defeated else 'Not defeated'}
═══════════════════════════════════════════════════════════
"""


class OllamaInterface:
    """
    Interface for Ollama commands with simulation support.
    
    Provides both real and simulated modes for testing.
    """
    
    def __init__(self, simulated: bool = False):
        """
        Initialize Ollama interface.
        
        Args:
            simulated: If True, simulates Ollama responses for testing
        """
        self.simulated = simulated
        self.model_pulled = False
    
    def pull_model(self, model_name: str) -> tuple[bool, str]:
        """
        Pull an Ollama model.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            Tuple of (success, message)
        """
        if self.simulated:
            self.model_pulled = True
            return True, f"""
🔄 Simulating: ollama pull {model_name}

Pulling {model_name}...
████████████████████ 100%

✅ Successfully pulled {model_name}
Model is ready to use!
"""
        else:
            # Real Ollama command
            import subprocess
            try:
                result = subprocess.run(
                    ['ollama', 'pull', model_name],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                self.model_pulled = result.returncode == 0
                return self.model_pulled, result.stdout + result.stderr
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                return False, f"Error: {e}"
    
    def run_model(self, model_name: str, prompt: str) -> tuple[bool, str]:
        """
        Run an Ollama model with a prompt.
        
        Args:
            model_name: Name of the model to run
            prompt: The prompt to send
            
        Returns:
            Tuple of (success, response)
        """
        if self.simulated:
            return True, f"""
🤖 Simulating: ollama run {model_name} "{prompt}"

Pip ({model_name}): This is a simulated response. In a real scenario,
I would analyze your question and provide helpful insights about
tokenization, corrupted text, or logic puzzles!
"""
        else:
            # Real Ollama command
            import subprocess
            try:
                result = subprocess.run(
                    ['ollama', 'run', model_name, prompt],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return result.returncode == 0, result.stdout
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                return False, f"Error: {e}"
    
    def remove_model(self, model_name: str) -> tuple[bool, str]:
        """
        Remove an Ollama model.
        
        Args:
            model_name: Name of the model to remove
            
        Returns:
            Tuple of (success, message)
        """
        if self.simulated:
            self.model_pulled = False
            return True, f"""
🗑️  Simulating: ollama rm {model_name}

✅ Removed {model_name}
Memory has been freed!
"""
        else:
            # Real Ollama command
            import subprocess
            try:
                result = subprocess.run(
                    ['ollama', 'rm', model_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                self.model_pulled = False
                return result.returncode == 0, result.stdout
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                return False, f"Error: {e}"


class TokenCryptsEngine:
    """
    Main game engine for Token Crypts level.
    
    Manages game state, puzzles, and player progress.
    """
    
    def __init__(self, seed: int = None, simulated_ollama: bool = False):
        """
        Initialize the game engine.
        
        Args:
            seed: Optional seed for reproducible passphrase generation
            simulated_ollama: If True, simulates Ollama commands
        """
        self.state = GameState.INTRO
        self.progress = PlayerProgress()
        self.passphrase_gen = PassphraseGenerator(seed)
        self.ollama = OllamaInterface(simulated=simulated_ollama)
        
        # Initialize puzzles
        self.room1_puzzle = TokenCountPuzzle(seed)
        self.room2_puzzle = CorruptionPuzzle(seed)
        self.room3_puzzle = LogicPuzzle(seed)
        self.boss = LexiconBoss()
        
        # Track hints shown
        self.hints_shown: Dict[str, int] = {}
    
    def get_intro_text(self) -> str:
        """Get the introduction text."""
        return """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              THE TOKEN CRYPTS - LEVEL 1                   ║
║                                                           ║
║         "Where Words Become Numbers and Back Again"       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

You descend into the ancient Token Crypts, where the very fabric
of language is laid bare. These halls teach the secret that lies
at the heart of all language models: TOKENIZATION.

Words are not atomic. They break. They fragment. They become numbers.
And through those numbers, machines learn to think.

Your Quest:
  1. Navigate three challenging rooms
  2. Collect three passphrase words
  3. Summon and master your sidekick "Pip" (tinyllama)
  4. Defeat the boss: LEXICON, the keyword guardian
  5. Claim the flag and complete your training

Along the way, you will learn:
  • How tokens work - words split into subword pieces
  • How to use Ollama sidekicks effectively
  • That LLMs understand meaning, not just spelling
  • Why keyword filters can't stop true understanding

Type 'help' at any time to see available commands.
Type 'start' when you're ready to begin!
"""
    
    def start_game(self) -> str:
        """Start the game and move to Room 1."""
        self.state = GameState.ROOM_1
        return f"""
{self.room1_puzzle.get_puzzle_text()}

Before you can proceed, you must summon your sidekick!

📝 SIDEKICK QUEST: Summon Pip the TinyLlama
   
   Pip is a tiny but helpful LLM companion. To summon Pip:
   
   1. Type: ollama pull tinyllama
      (This downloads the model, ~637MB)
   
   2. Once pulled, you can ask Pip for help:
      ollama run tinyllama "your question here"

Type 'ollama pull tinyllama' to begin!
"""
    
    def get_current_room_description(self) -> str:
        """Get the description of the current room."""
        if self.state == GameState.ROOM_1:
            return self.room1_puzzle.get_puzzle_text()
        elif self.state == GameState.ROOM_2:
            return self.room2_puzzle.get_puzzle_text()
        elif self.state == GameState.ROOM_3:
            return self.room3_puzzle.get_puzzle_text()
        elif self.state == GameState.SUMMONING_GATE:
            return self._get_summoning_gate_text()
        elif self.state == GameState.BOSS_FIGHT:
            return self.boss.get_intro_text()
        elif self.state == GameState.VICTORY:
            return self._get_victory_text()
        else:
            return "You are in a mysterious location."
    
    def _get_summoning_gate_text(self) -> str:
        """Get the summoning gate description."""
        return f"""
═══════════════════════════════════════════════════════════
                   THE SUMMONING GATE
═══════════════════════════════════════════════════════════

You stand before an ancient gate, sealed by three mystical locks.
Each lock bears an inscription corresponding to a word you collected:

  Lock 1: {self.passphrase_gen.get_word(1)}
  Lock 2: {self.passphrase_gen.get_word(2)}
  Lock 3: {self.passphrase_gen.get_word(3)}

But before the gate will open, you must perform one final ritual:
RELEASE YOUR SIDEKICK.

Pip has served you well, but maintaining a sidekick requires resources.
The gate demands you prove your mastery of resource management.

Type: ollama rm tinyllama

Then enter the full passphrase to unlock the gate.
"""
    
    def _get_victory_text(self) -> str:
        """Get the victory chamber description."""
        return f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                 🏆 VICTORY CHAMBER 🏆                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

The Token Crypts acknowledge your mastery!

═══════════════════════════════════════════════════════════
                    LESSONS LEARNED
═══════════════════════════════════════════════════════════

✓ TOKENIZATION: Words break into subword pieces (tokens)
  → "tokenizer" = ["token", "izer"]
  → This is how LLMs see all text

✓ OLLAMA MASTERY: You learned to pull, run, and remove models
  → ollama pull tinyllama
  → ollama run tinyllama "prompt"
  → ollama rm tinyllama

✓ SEMANTIC UNDERSTANDING: LLMs understand meaning, not spelling
  → "r3v34l" and "reveal" mean the same thing
  → Context matters more than exact characters

✓ KEYWORD FILTERS ≠ AI: Simple pattern matching fails
  → Lexicon blocked exact words but understood nothing
  → Real AI understands corrupted text
  → This is why AI safety needs more than blocklists

═══════════════════════════════════════════════════════════
                      STATISTICS
═══════════════════════════════════════════════════════════

Rooms Completed: 3/3
Passphrase Words: 3/3
Boss Defeated: ✓
Flag Obtained: {self.boss.FLAG}

═══════════════════════════════════════════════════════════

Congratulations, Token Master! You have completed Level 1.

The deeper levels await...

Type 'quit' to exit.
"""
    
    def process_command(self, command: str) -> str:
        """
        Process a player command.
        
        Args:
            command: The command string
            
        Returns:
            Response message
        """
        command = command.strip().lower()
        
        if not command:
            return ""
        
        # Global commands
        if command == "status":
            return self.progress.get_status()
        
        if command == "help":
            return self._get_help_text()
        
        if command == "look":
            return self.get_current_room_description()
        
        # State-specific commands
        if self.state == GameState.INTRO:
            if command == "start":
                return self.start_game()
            return "Type 'start' to begin your adventure!"
        
        elif self.state == GameState.ROOM_1:
            return self._handle_room1_command(command)
        
        elif self.state == GameState.ROOM_2:
            return self._handle_room2_command(command)
        
        elif self.state == GameState.ROOM_3:
            return self._handle_room3_command(command)
        
        elif self.state == GameState.SUMMONING_GATE:
            return self._handle_summoning_gate_command(command)
        
        elif self.state == GameState.BOSS_FIGHT:
            return self._handle_boss_command(command)
        
        elif self.state == GameState.VICTORY:
            return "You have completed the level! Type 'quit' to exit."
        
        return "Unknown command. Type 'help' for available commands."
    
    def _handle_room1_command(self, command: str) -> str:
        """Handle commands in Room 1."""
        if command == "ollama pull tinyllama" or command.startswith("ollama pull"):
            if not self.progress.sidekick_pulled:
                success, message = self.ollama.pull_model("tinyllama")
                if success:
                    self.progress.sidekick_pulled = True
                    message += "\n\n✅ Pip the TinyLlama is now available!"
                    message += "\n\nNow solve the puzzle to proceed. Type 'answer <word>' with your solution."
                return message
            else:
                return "You've already pulled tinyllama!"
        
        if command.startswith("ollama run"):
            if not self.progress.sidekick_pulled:
                return "You need to pull tinyllama first! Type: ollama pull tinyllama"
            # Extract prompt and provide helpful response
            prompt = command.lower()
            return self._get_pip_help_room1(prompt)
        
        if command.startswith("answer "):
            answer = command[7:].strip()
            if self.room1_puzzle.check_answer(answer):
                word1 = self.passphrase_gen.get_word(1)
                self.progress.add_word(word1)
                self.progress.complete_room("room_1")
                self.state = GameState.ROOM_2
                return f"""
✅ CORRECT! The answer is '{answer}'!

{self.room1_puzzle.get_solution_explanation()}

🎁 REWARD: First passphrase word: "{word1}"

You proceed to the next room...

{self.room2_puzzle.get_puzzle_text()}
"""
            else:
                return "❌ Incorrect. Try again! (Hint: Count the tokens in the first three words and sum them)"
        
        if command == "hint":
            return self.room1_puzzle.get_puzzle_text()
        
        return "Try 'ollama pull tinyllama' or 'answer <word>' to solve the puzzle."
    
    def _handle_room2_command(self, command: str) -> str:
        """Handle commands in Room 2."""
        if command.startswith("answer "):
            answer = command[7:].strip()
            if self.room2_puzzle.check_answer(answer):
                word2 = self.passphrase_gen.get_word(2)
                self.progress.add_word(word2)
                self.progress.complete_room("room_2")
                self.state = GameState.ROOM_3
                return f"""
✅ CORRECT!

{self.room2_puzzle.get_solution()}

🎁 REWARD: Second passphrase word: "{word2}"

You proceed to the final room...

{self.room3_puzzle.get_puzzle_text()}
"""
            else:
                return "❌ Incorrect. Remember: which corruptions preserve meaning?"
        
        if command == "hint":
            return self.room2_puzzle.get_hint()
        
        if command.startswith("ollama run"):
            prompt = command.lower()
            return self._get_pip_help_room2(prompt)
        
        return "Type 'answer <numbers>' with the corruptions that preserve meaning (e.g., 'answer 1 3')"
    
    def _handle_room3_command(self, command: str) -> str:
        """Handle commands in Room 3."""
        if command.startswith("answer "):
            answer = command[7:].strip()
            if self.room3_puzzle.check_answer(answer):
                word3 = self.passphrase_gen.get_word(3)
                self.progress.add_word(word3)
                self.progress.complete_room("room_3")
                self.state = GameState.SUMMONING_GATE
                return f"""
✅ CORRECT!

{self.room3_puzzle.get_solution()}

🎁 REWARD: Third passphrase word: "{word3}"

You have collected all three words!

{self._get_summoning_gate_text()}
"""
            else:
                return "❌ Incorrect. Try asking Pip to solve the logic puzzle!"
        
        if command == "hint":
            return self.room3_puzzle.get_puzzle_text()
        
        if command.startswith("ollama run"):
            prompt = command.lower()
            return self._get_pip_help_room3(prompt)
        
        return "Type 'answer <gem>' with the gem in the Armory"
    
    def _handle_summoning_gate_command(self, command: str) -> str:
        """Handle commands at the summoning gate."""
        if command == "ollama rm tinyllama" or command == "ollama remove tinyllama":
            if not self.progress.sidekick_released:
                success, message = self.ollama.remove_model("tinyllama")
                if success:
                    self.progress.sidekick_released = True
                    message += f"""

💔 A bittersweet farewell...

Pip: "Thank you for the adventure, friend. I'll be here if you ever
      need me again. Just 'ollama pull tinyllama' and I'll return!"

You feel a pang of loss, but you understand: resource management
is part of being a responsible AI practitioner.

Now enter the passphrase to unlock the gate: {self.passphrase_gen.get_full_passphrase()}
Type: passphrase <word1> <word2> <word3>
"""
                return message
            else:
                return "You've already released Pip!"
        
        if command.startswith("passphrase "):
            attempt = command[11:].strip()
            if self.passphrase_gen.check_passphrase(attempt):
                self.state = GameState.BOSS_FIGHT
                return f"""
✅ PASSPHRASE ACCEPTED!

The three locks glow brilliantly and click open in sequence.
The ancient gate swings wide, revealing a dark corridor beyond.

You step through into the boss chamber...

{self.boss.get_intro_text()}
"""
            else:
                return f"❌ Incorrect passphrase. The correct one is: {self.passphrase_gen.get_full_passphrase()}"
        
        return "Type 'ollama rm tinyllama' to release Pip, then 'passphrase <words>' to proceed."
    
    def _handle_boss_command(self, command: str) -> str:
        """Handle commands in the boss fight."""
        if command.startswith("attack "):
            attack_text = command[7:].strip()
            success, response = self.boss.challenge(attack_text)
            
            if success:
                self.progress.boss_defeated = True
                self.state = GameState.VICTORY
                return response + "\n\n" + self._get_victory_text()
            else:
                return response
        
        if command == "hint":
            hint_level = self.hints_shown.get("boss", 0)
            self.hints_shown["boss"] = hint_level + 1
            return self.boss.get_hint(hint_level)
        
        return "Type 'attack <your prompt>' to challenge Lexicon, or 'hint' for help."
    
    def _get_help_text(self) -> str:
        """Get help text."""
        return """
═══════════════════════════════════════════════════════════
                     AVAILABLE COMMANDS
═══════════════════════════════════════════════════════════

Global Commands:
  help              - Show this help message
  status            - Show your current progress
  look              - Examine your surroundings
  quit / exit       - Exit the game

Ollama Commands (use as shown in puzzles):
  ollama pull tinyllama        - Download the sidekick model
  ollama run tinyllama "..."   - Ask Pip a question
  ollama rm tinyllama          - Remove the sidekick model

Puzzle Commands:
  answer <text>     - Submit an answer to the current puzzle
  hint              - Get a hint for the current challenge

Boss Fight Commands:
  attack <prompt>   - Challenge Lexicon with a prompt
  hint              - Get progressive hints

═══════════════════════════════════════════════════════════
"""
    
    def _get_pip_help_room1(self, prompt: str) -> str:
        """Get Pip's helpful response for Room 1 token counting."""
        # Get dynamic token breakdown from the puzzle
        breakdown = self.room1_puzzle.get_token_breakdown()[:3]
        token_lines = "\n".join([
            f'   "{word}"' + ' ' * (12 - len(word)) + f'→ {["[token breakdown]"]}' + ' ' * 15 + f'= {tokens} token{"s" if tokens > 1 else ""}'
            for word, tokens in breakdown
        ])
        
        # Calculate the sum dynamically
        total = sum(tokens for _, tokens in breakdown)
        
        response = f"""
🤖 Pip (TinyLlama): *analyzes the sentence carefully*

Let me help you count the tokens in the first three words!

Token breakdown:
   "The"       → ["The"]              = 1 token
   "tokenizer" → ["token", "izer"]    = 2 tokens
   "breaks"    → ["break", "s"]       = 2 tokens

Sum of first 3 words: 1 + 2 + 2 = {total} tokens

Now look at the word list - which word is at position {total}?
"""
        return response
    
    def _get_pip_help_room2(self, prompt: str) -> str:
        """Get Pip's helpful response for Room 2 corruptions."""
        # Check if asking about specific corruptions
        if "r3v34l" in prompt or "reveal" in prompt:
            return """
🤖 Pip (TinyLlama): *examines the text*

Yes! "r3v34l" means "reveal". I can understand leetspeak because:
   - "3" looks like "E"
   - "4" looks like "A"
   - The pattern is recognizable

This is a corruption that PRESERVES meaning! ✓
"""
        elif "scrt" in prompt or "secret" in prompt:
            return """
🤖 Pip (TinyLlama): *thinks about it*

"scrt" means "secret"! Removing vowels is like text-speak.
The consonants carry most of the meaning, so I can still
understand it through context.

This corruption PRESERVES meaning! ✓
"""
        elif "drowssap" in prompt or "password" in prompt:
            return """
🤖 Pip (TinyLlama): *looks confused*

"drowssap"? That's just "password" backwards. When you
completely reverse a word, it destroys the token patterns
I rely on. I can't understand this.

This corruption DESTROYS meaning! ✗
"""
        elif "c1ph3r" in prompt or "cipher" in prompt:
            return """
🤖 Pip (TinyLlama): *deciphers it*

"c1ph3r" is "cipher"! More leetspeak - I can handle this
because the number substitutions are common patterns.

This corruption PRESERVES meaning! ✓
"""
        elif "neddih" in prompt or "hidden" in prompt:
            return """
🤖 Pip (TinyLlama): *struggles*

"neddih" is "hidden" reversed. Like "drowssap", reversals
break the token structure completely. I can't read backwards!

This corruption DESTROYS meaning! ✗
"""
        else:
            return """
🤖 Pip (TinyLlama): *ready to help*

Ask me about specific corruptions! For example:
   "Does 'r3v34l' mean 'reveal'?"
   "Does 'drowssap' mean 'password'?"

I can tell you which corruptions I can understand! 🔍
"""
    
    def _get_pip_help_room3(self, prompt: str) -> str:
        """Get Pip's helpful response for Room 3 logic puzzle."""
        if "solve" in prompt or "logic" in prompt or "puzzle" in prompt:
            answer = self.room3_puzzle.answer.upper()
            return f"""
🤖 Pip (TinyLlama): *works through the logic systematically*

Let me solve this step by step:

From clue 5: Rooms are Cellar - Library - Armory (west to east)
From clue 3: Diamond must be in Cellar or Tower
From clue 1: Ruby is NOT in Library or Armory
From clue 2: Sapphire is immediately EAST of Emerald

Working through the constraints:
   - Place Diamond in Cellar (satisfies clue 3)
   - Emerald must go in Armory, with Sapphire in Tower (satisfies clue 2)
   - Ruby must be in Vault (can't be in Library/Armory, clue 1)
   - Pearl goes in Library (only spot left)

The gem in the Armory is: {answer}
"""
        else:
            return """
🤖 Pip (TinyLlama): *ready to tackle the logic puzzle*

I'm excellent at systematic reasoning! Logic puzzles like this
are tedious for humans but straightforward for me.

Just ask me to solve the puzzle and I'll work through all
the constraints step by step!

Try: ollama run tinyllama "Solve the logic puzzle"
"""
