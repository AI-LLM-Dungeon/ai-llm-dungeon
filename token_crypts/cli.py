"""Command-line interface for Token Crypts level."""

import sys
from typing import Optional
from .game_engine import TokenCryptsEngine, GameState


class TokenCryptsCLI:
    """
    Command-line interface for playing Token Crypts.
    
    Handles user input, displays game state, and manages the game loop.
    """
    
    # ANSI color codes
    COLOR_RESET = '\033[0m'
    COLOR_CYAN = '\033[96m'
    COLOR_GREEN = '\033[92m'
    COLOR_YELLOW = '\033[93m'
    COLOR_RED = '\033[91m'
    COLOR_MAGENTA = '\033[95m'
    COLOR_BOLD = '\033[1m'
    
    def __init__(self, seed: Optional[int] = None, simulated: bool = False):
        """
        Initialize the CLI.
        
        Args:
            seed: Optional seed for reproducible gameplay
            simulated: If True, simulates Ollama commands for testing
        """
        self.engine = TokenCryptsEngine(seed=seed, simulated_ollama=simulated)
        self.running = True
    
    def start(self) -> None:
        """Start the CLI and enter the main game loop."""
        self._display_banner()
        print(self.engine.get_intro_text())
        
        # Main game loop
        while self.running:
            try:
                # Get prompt based on game state
                prompt = self._get_prompt()
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Check for quit commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    self._handle_quit()
                    break
                
                # Process command
                response = self.engine.process_command(user_input)
                if response:
                    print(response)
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Type 'quit' to exit properly.")
                continue
            except EOFError:
                print("\n\nGame ended.")
                break
            except Exception as e:
                print(f"\n{self.COLOR_RED}Error: {e}{self.COLOR_RESET}")
                print("Please try again or type 'help' for commands.")
    
    def _display_banner(self) -> None:
        """Display the game banner."""
        banner = f"""
{self.COLOR_CYAN}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              THE TOKEN CRYPTS - LEVEL 1                   ║
║                                                           ║
║         "Where Words Become Numbers and Back Again"       ║
║                                                           ║
║                   AI-LLM-DUNGEON                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{self.COLOR_RESET}
"""
        print(banner)
    
    def _get_prompt(self) -> str:
        """Get the command prompt based on current game state."""
        state_prompts = {
            GameState.INTRO: f"{self.COLOR_GREEN}[Entrance]>{self.COLOR_RESET} ",
            GameState.ROOM_1: f"{self.COLOR_YELLOW}[Room 1 - Syllable Sanctuary]>{self.COLOR_RESET} ",
            GameState.ROOM_2: f"{self.COLOR_YELLOW}[Room 2 - Subword Sewers]>{self.COLOR_RESET} ",
            GameState.ROOM_3: f"{self.COLOR_YELLOW}[Room 3 - Cipher Chamber]>{self.COLOR_RESET} ",
            GameState.SUMMONING_GATE: f"{self.COLOR_MAGENTA}[Summoning Gate]>{self.COLOR_RESET} ",
            GameState.BOSS_FIGHT: f"{self.COLOR_RED}[BOSS - Lexicon]>{self.COLOR_RESET} ",
            GameState.VICTORY: f"{self.COLOR_GREEN}[Victory!]>{self.COLOR_RESET} ",
        }
        return state_prompts.get(self.engine.state, "> ")
    
    def _handle_quit(self) -> None:
        """Handle quit command."""
        print(f"\n{self.COLOR_CYAN}Thank you for playing Token Crypts!{self.COLOR_RESET}")
        print("Your journey through the realm of tokenization continues...")
        print("\nProgress has been saved to memory. Farewell, adventurer!")
        self.running = False


def main():
    """Main entry point for the CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Token Crypts - Learn about LLM tokenization through adventure'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='Seed for reproducible passphrase generation',
        default=None
    )
    parser.add_argument(
        '--simulated',
        action='store_true',
        help='Use simulated Ollama mode (for testing without Ollama installed)'
    )
    
    args = parser.parse_args()
    
    try:
        cli = TokenCryptsCLI(seed=args.seed, simulated=args.simulated)
        cli.start()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
