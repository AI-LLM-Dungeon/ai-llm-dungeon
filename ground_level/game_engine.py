"""Game engine for the Ground Level of AI-LLM-Dungeon."""

import json
import os
import time
from typing import Dict, Optional, List
from .player import Player
from .sidekick import Sidekick
from .puzzle import Puzzle
from .room import Room, create_room
from .ollama_simulator import OllamaSimulator
from .ascii_art import display_banner, display_victory, display_room_transition, display_shaman, slow_print, display_certificate, display_descend

# Import shared navigation system
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.navigation import show_descend_menu
from game.commands import StandardCommands

# ANSI color codes for terminal output
COLOR_CYAN = '\033[96m'
COLOR_RESET = '\033[0m'


class GameEngine:
    """
    Main game engine that manages the Ground Level game state and flow.
    
    Handles loading data, managing rooms, processing player commands,
    and coordinating all game systems.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the game engine.
        
        Args:
            data_dir: Directory containing JSON data files
        """
        self.data_dir = data_dir
        self.player = Player()
        self.sidekicks: Dict[str, Sidekick] = {}
        self.puzzles: Dict[str, Puzzle] = {}
        self.tips: Dict[str, dict] = {}
        self.current_room: Optional[Room] = None
        self.ollama = OllamaSimulator()
        self.game_running = True
        self.standard_commands = StandardCommands()  # Standard command helper
        
        # Load all game data
        self._load_data()
        
        # Initialize first room (Ollama Village)
        self.current_room = create_room(0)
    
    def _load_data(self) -> None:
        """Load all JSON data files."""
        # Load sidekicks/models
        models_path = os.path.join(self.data_dir, "models.json")
        with open(models_path, 'r') as f:
            models_data = json.load(f)
            for model_data in models_data:
                sidekick = Sidekick.from_dict(model_data)
                self.sidekicks[sidekick.name] = sidekick
        
        # Load puzzles
        puzzles_path = os.path.join(self.data_dir, "puzzles.json")
        with open(puzzles_path, 'r') as f:
            puzzles_data = json.load(f)
            for puzzle_data in puzzles_data:
                puzzle = Puzzle.from_dict(puzzle_data)
                self.puzzles[puzzle.id] = puzzle
        
        # Load tips
        tips_path = os.path.join(self.data_dir, "tips.json")
        with open(tips_path, 'r') as f:
            tips_data = json.load(f)
            for tip in tips_data:
                self.tips[tip["id"]] = tip
    
    def start(self) -> None:
        """Start the game and enter the main game loop."""
        display_banner()
        print("\nWelcome, brave adventurer!")
        print("You are about to embark on a journey to master Ollama and local LLMs.")
        print("\nType 'help' at any time to see available commands.\n")
        
        input("Press Enter to begin your quest...")
        
        # Enter the first room
        self.current_room.enter(self.player)
        
        # Main game loop
        self.game_loop()
    
    def game_loop(self) -> None:
        """Main game loop that processes player commands."""
        while self.game_running:
            try:
                # Show prompt
                prompt = f"\n[Room {self.player.current_room}]> "
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Process command
                self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Type 'quit' to exit properly.")
            except Exception as e:
                print(f"\n⚠️  An error occurred: {e}")
                print("Please try again or type 'help' for available commands.")
    
    def process_command(self, command: str) -> None:
        """
        Process a player command.
        
        Args:
            command: The command string entered by the player
        """
        command = command.lower().strip()
        
        # Basic commands
        if command in ["quit", "exit"]:
            self._handle_quit()
        elif command == "help":
            self._handle_help()
        elif command == "status":
            self._handle_status()
        elif command == "tips":
            self._handle_tips()
        elif command in ["look", "l"]:
            self._handle_look()
        elif command == "ls":
            self._handle_ls()
        elif command == "pwd":
            self._handle_pwd()
        elif command == "map":
            self._handle_map()
        
        # Room 0: Ollama Village
        elif self.player.current_room == 0:
            self._handle_room0_commands(command)
        
        # Room 1: Summoning Chamber
        elif self.player.current_room == 1:
            self._handle_room1_commands(command)
        
        # Room 2: Riddle Hall
        elif self.player.current_room == 2:
            self._handle_room2_commands(command)
        
        # Room 3: Upgrade Forge
        elif self.player.current_room == 3:
            self._handle_room3_commands(command)
        
        # Room 4: Victory Chamber
        elif self.player.current_room == 4:
            self._handle_room4_commands(command)
        
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")
    
    def _handle_room0_commands(self, command: str) -> None:
        """Handle commands specific to Room 0 (Ollama Village)."""
        
        # Room 0: User types 'learn' to begin (only time 'learn' is used)
        if command in ["learn", "teach", "lesson", "next"]:
            if not self.player.has_completed_objective("room0_lesson1_taught"):
                display_shaman()
                self._teach_install()
                self.player.complete_objective("room0_lesson1_taught")
            else:
                print("\n💡 Hint: You've already started your training!")
                print("Try practicing the commands you've learned.")
        
        # Lesson 1: User must type 'ollama' to complete
        elif command == "ollama":
            if not self.player.has_completed_objective("room0_lesson1_taught"):
                print("\n⚠️  Please type 'learn' first to begin your training.")
            elif self.player.has_completed_objective("room0_lesson1"):
                print("\n✅ You've already learned this command! Continue with the next lesson.")
            else:
                display_shaman()
                self._complete_lesson1()
        
        # Lesson 2: User must type 'ollama serve' to complete
        elif command == "ollama serve":
            if not self.player.has_completed_objective("room0_lesson2"):
                if not self.player.has_completed_objective("room0_lesson1"):
                    print("\n⚠️  Please complete the previous lessons first.")
                else:
                    display_shaman()
                    self._complete_lesson2()
            else:
                print("\n✅ You've already learned this command! Continue with the next lesson.")
        
        # Lesson 3: User must type 'ollama list' to complete
        elif command == "ollama list":
            if not self.player.has_completed_objective("room0_lesson3"):
                if not self.player.has_completed_objective("room0_lesson2"):
                    print("\n⚠️  Please complete the previous lessons first.")
                else:
                    display_shaman()
                    self._complete_lesson3()
            else:
                # Allow list command anytime after lesson 3
                self.ollama.list_models()
        
        # Lesson 4: User must type 'ollama pull phi3:mini' to complete
        elif command == "ollama pull phi3:mini":
            if not self.player.has_completed_objective("room0_lesson4"):
                if not self.player.has_completed_objective("room0_lesson3"):
                    print("\n⚠️  Please complete the previous lessons first.")
                else:
                    display_shaman()
                    self._complete_lesson4()
            else:
                # Allow pull command anytime after lesson 4
                self.ollama.pull_model("phi3-mini")
        
        # Lesson 5: User must type 'ollama run phi3:mini' to complete
        elif command == "ollama run phi3:mini":
            if not self.player.has_completed_objective("room0_lesson5"):
                if not self.player.has_completed_objective("room0_lesson4"):
                    print("\n⚠️  Please complete the previous lessons first.")
                else:
                    display_shaman()
                    self._complete_lesson5()
            else:
                print("\n✅ You've already learned this command!")
        
        # Lesson 6: User must type 'ollama show phi3:mini' to complete
        elif command == "ollama show phi3:mini":
            if not self.player.has_completed_objective("room0_lesson6"):
                if not self.player.has_completed_objective("room0_lesson5"):
                    print("\n⚠️  Please complete the previous lessons first.")
                else:
                    display_shaman()
                    self._complete_lesson6()
            else:
                # Allow show command anytime after lesson 6
                self.ollama.show_model("phi3-mini")
        
        # Lesson 7: User must type 'ollama rm phi3:mini' to complete
        elif command == "ollama rm phi3:mini":
            if not self.player.has_completed_objective("room0_lesson7"):
                if not self.player.has_completed_objective("room0_lesson6"):
                    print("\n⚠️  Please complete the previous lessons first.")
                else:
                    display_shaman()
                    self._complete_lesson7()
            else:
                # Allow rm command anytime after lesson 7
                self.ollama.remove_model("phi3-mini")
        
        elif command == "east":
            if self.player.has_completed_objective("room0_complete"):
                self._move_to_room(1)
            else:
                print("\n⚠️  The Shaman blocks your path.")
                print("'You must complete all lessons first, young one.'")
                if not self.player.has_completed_objective("room0_lesson1_taught"):
                    print("Hint: Type 'learn' to begin your training.")
                else:
                    print("Hint: Practice the commands you've learned!")
        
        else:
            print(f"\nUnknown command. Type 'help' for available commands.")
            if not self.player.has_completed_objective("room0_lesson1_taught"):
                print("Hint: Type 'learn' to receive the Shaman's teachings!")
    
    def _teach_install(self) -> None:
        """Teach the player about installing Ollama."""
        
        slow_print("\n=== LESSON 1: Installing Ollama ===\n", 0.5)
        slow_print("The Shaman speaks:")
        slow_print("'Before you can wield the power of local LLMs, you must first")
        slow_print("install the Ollama tool on your system.'\n")
        
        slow_print("'This dungeon is a SIMULATION that teaches you the exact commands")
        slow_print("you'll need when you're ready to install Ollama for real.")
        slow_print("No installation is required to play this game!'\n")
        
        slow_print("For installation instructions when you're ready, visit:")
        slow_print("  https://ollama.com/download\n")
        
        slow_print("'Once installed and running, all commands inside Ollama begin with \"ollama\".")
        slow_print("Ollama gives you command-line access to powerful language models")
        slow_print("that run entirely on your own machine.'\n")
        
        slow_print("Now, let's practice the command. Type: ollama")
    
    def _complete_lesson1(self) -> None:
        """Complete lesson 1 by typing 'ollama'."""
        
        print("\n✅ Correct! The `ollama` command is your gateway to LLM management.")
        print()
        
        self.player.complete_objective("room0_lesson1")
        
        slow_print("=== LESSON 2: Starting the Ollama Service ===\n", 0.5)
        slow_print("The Shaman demonstrates:")
        slow_print("'The `ollama serve` command starts the Ollama daemon in the background.")
        slow_print("This service listens for requests and manages your LLM models.")
        slow_print("On most systems, this starts automatically, but it's good to know!'\n")
        
        slow_print("Now, practice this command. Type: ollama serve")
    
    def _complete_lesson2(self) -> None:
        """Complete lesson 2 by typing 'ollama serve'."""
        
        print()
        self.ollama.serve()
        print()
        
        self.player.complete_objective("room0_lesson2")
        
        slow_print("✅ Lesson 2 Complete!\n", 0.5)
        slow_print("=== LESSON 3: Listing Your Models ===\n")
        slow_print("The Shaman explains:")
        slow_print("'To see which models you have installed, use: ollama list'")
        slow_print("'This command will be useful to verify your models after pulling them.'\n")
        
        slow_print("Practice this command now. Type: ollama list")
    
    def _complete_lesson3(self) -> None:
        """Complete lesson 3 by typing 'ollama list'."""
        
        print()
        self.ollama.list_models()
        print()
        
        self.player.complete_objective("room0_lesson3")
        
        slow_print("✅ Lesson 3 Complete!\n", 0.5)
        slow_print("The Shaman nods:")
        slow_print("'You haven't pulled any models yet. Let's learn how to do that next!\n")
        
        slow_print("=== LESSON 4: Pulling (Downloading) Models ===\n")
        slow_print("The Shaman teaches the most important command:")
        slow_print("'To download a model, use: ollama pull <model-name>'")
        slow_print("'Each model has a size - smaller models are faster but less capable.")
        slow_print("Phi3 Mini is about 2.3 GB. Larger models like Llama3 are 4-5 GB.")
        slow_print("Choose based on your needs and available disk space!'\n")
        
        slow_print("Now, let's pull the phi3:mini model. Type: ollama pull phi3:mini")
    
    def _complete_lesson4(self) -> None:
        """Complete lesson 4 by typing 'ollama pull phi3:mini'."""
        
        print()
        self.ollama.pull_model("phi3-mini")
        print()
        
        self.player.complete_objective("room0_lesson4")
        
        slow_print("✅ Lesson 4 Complete!\n", 0.5)
        slow_print("=== LESSON 5: Running Models ===\n")
        slow_print("The Shaman demonstrates:")
        slow_print("'Once a model is pulled, you can chat with it using: ollama run <model-name>'\n")
        
        slow_print("Example:")
        slow_print("  $ ollama run phi3:mini")
        slow_print("  >>> Tell me about AI")
        slow_print("  [The model responds with information about AI...]")
        slow_print("  >>> /bye\n")
        
        slow_print("'This is how you interact with your local LLM assistants!'\n")
        
        slow_print("Practice running the model. Type: ollama run phi3:mini")
    
    def _complete_lesson5(self) -> None:
        """Complete lesson 5 by typing 'ollama run phi3:mini'."""
        
        print()
        slow_print("🤖 Simulating: ollama run phi3:mini\n", 0.5)
        slow_print("Sidekick phi3:mini activated successfully!")
        print()
        
        self.player.complete_objective("room0_lesson5")
        
        slow_print("✅ Lesson 5 Complete!\n", 0.5)
        slow_print("=== LESSON 6: Inspecting Model Information ===\n")
        slow_print("The Shaman demonstrates:")
        slow_print("'To see detailed information about a model, use: ollama show <model-name>'")
        slow_print("'This displays the model's architecture, parameters, and configuration.")
        slow_print("It's useful for understanding what you're working with!'\n")
        
        slow_print("Example:")
        slow_print("  $ ollama show phi3:mini")
        slow_print("  [Shows model architecture, parameters, quantization, etc...]\n")
        
        slow_print("Practice inspecting the model. Type: ollama show phi3:mini")
    
    def _complete_lesson6(self) -> None:
        """Complete lesson 6 by typing 'ollama show phi3:mini'."""
        
        print()
        self.ollama.show_model("phi3-mini")
        print()
        
        self.player.complete_objective("room0_lesson6")
        
        slow_print("✅ Lesson 6 Complete!\n", 0.5)
        slow_print("=== LESSON 7: Removing Models ===\n")
        slow_print("The Shaman explains the final command:")
        slow_print("'Models take up disk space. When you no longer need one,")
        slow_print("you can remove it with: ollama rm <model-name>'")
        slow_print("'This frees up space for other models. You can always pull it again later!")
        slow_print("Good model management keeps your system tidy and efficient.'\n")
        
        slow_print("Practice removing the model. Type: ollama rm phi3:mini")
    
    def _complete_lesson7(self) -> None:
        """Complete lesson 7 by typing 'ollama rm phi3:mini'."""
        
        print()
        self.ollama.remove_model("phi3-mini")
        print()
        
        self.player.complete_objective("room0_lesson7")
        self.player.complete_objective("room0_complete")
        self.current_room.mark_completed()
        
        slow_print("✅ Lesson 7 Complete!\n", 0.5)
        slow_print("The Shaman smiles warmly:")
        slow_print("'You have learned all the essential Ollama commands!")
        slow_print("You are now ready to face the challenges ahead.'\n")
        
        slow_print("🎓 TRAINING COMPLETE! 🎓")
        slow_print("You may now proceed east to the Summoning Chamber.")
        slow_print("Type 'east' when you are ready.\n")
    
    def _handle_room1_commands(self, command: str) -> None:
        """Handle commands specific to Room 1 (Summoning Chamber)."""
        
        # Check for real Ollama command
        phi3 = self.sidekicks["Phi3 Mini"]
        
        if command == "ollama pull phi3:mini" or command == phi3.summon_scroll.lower():
            if not self.player.has_completed_objective("room1_pulled"):
                # Correct summon command - pull the model first
                print("\n📥 Pulling the Phi3 Mini model...")
                self.ollama.pull_model("phi3-mini")
                
                # Then summon
                print(phi3.summon())
                self.player.set_active_sidekick(phi3)
                
                # Mark pull objective complete
                self.player.complete_objective("room1_pulled")
                
                print()
                slow_print("✅ Model pulled successfully!\n", 0.5)
                slow_print("Before continuing, verify your model is ready.")
                slow_print("Type: ollama list")
            else:
                print("\n✅ You've already pulled this model!")
                print("Try: ollama list")
        
        elif command == "ollama list":
            if not self.player.has_completed_objective("room1_pulled"):
                print("\n⚠️  You need to pull a model first!")
                print("Try: ollama pull phi3:mini")
            else:
                print()
                self.ollama.list_models()
                
                if not self.player.has_completed_objective("room1_complete"):
                    print()
                    slow_print("✅ Perfect! You can see phi3-mini is now available as a sidekick.", 0.5)
                    slow_print("This command helps you track which models are ready to use.")
                    
                    # Unlock tip
                    self.player.unlock_tip("tip_04", self.tips["tip_04"]["text"])
                    
                    # Mark objective complete
                    self.player.complete_objective("room1_complete")
                    self.current_room.mark_completed()
                    
                    print()
                    slow_print("✅ Objective Complete!")
                    slow_print("You've learned to summon a sidekick using Ollama commands.")
                    slow_print("\nYou can now proceed to the next room.")
                    slow_print("Type 'east' to continue your journey.")
        
        elif command == "west":
            self._move_to_room(0)
        
        elif command == "east":
            if self.player.has_completed_objective("room1_complete"):
                self._move_to_room(2)
            else:
                print("\n⚠️  You must complete this room's objectives first!")
                if not self.player.has_completed_objective("room1_pulled"):
                    print("Try: ollama pull phi3:mini")
                else:
                    print("Try: ollama list")
        
        elif "ollama" in command and "pull" in command:
            print("\n❌ That's not quite right.")
            print("Make sure to use the exact command: ollama pull phi3:mini")
        
        elif "summon" in command:
            print("\n💡 Hint: In the real world, we use Ollama commands, not scroll text!")
            print("Try: ollama pull phi3:mini")
        
        else:
            print(f"\nUnknown command. Type 'help' for available commands.")
            if not self.player.has_completed_objective("room1_pulled"):
                print("Hint: Try the command shown on the scroll: ollama pull phi3:mini")
            else:
                print("Hint: Verify your models with: ollama list")
    
    def _handle_room2_commands(self, command: str) -> None:
        """Handle commands specific to Room 2 (Riddle Hall)."""
        if command == "west":
            self._move_to_room(1)
        
        elif command == "east":
            if self.player.has_completed_objective("room2_complete"):
                self._move_to_room(3)
            else:
                print("⚠️  You must complete this room's objectives first!")
        
        elif command == "ollama run phi3:mini":
            self._run_phi3_riddle()
        
        elif command == "ollama run llama3:8b":
            self._run_llama3_riddle()
        
        elif command in ["riddle", "attempt", "try riddle", "solve"]:
            print("💡 Hint: Use the Ollama run command to consult your sidekick!")
            if self.player.active_sidekick:
                if self.player.active_sidekick.name == "Phi3 Mini":
                    print("Try: ollama run phi3:mini")
                elif self.player.active_sidekick.name == "Llama3 8b":
                    print("Try: ollama run llama3:8b")
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            if self.player.active_sidekick:
                if self.player.active_sidekick.name == "Phi3 Mini":
                    print("Hint: Try 'ollama run phi3:mini' to consult your sidekick!")
                elif self.player.active_sidekick.name == "Llama3 8b":
                    print("Hint: Try 'ollama run llama3:8b' to consult your sidekick!")
    
    def _handle_room3_commands(self, command: str) -> None:
        """Handle commands specific to Room 3 (Upgrade Forge)."""
        if command == "west":
            self._move_to_room(2)
        
        elif command == "east":
            if not self.player.has_completed_objective("room3_complete"):
                print("⚠️  You must complete this room's objectives first!")
            elif not self.player.has_discovered_password():
                print("⚠️  The Victory Chamber is locked!")
                print("You need to discover the password first.")
                print("Hint: Go WEST to the Riddle Hall and use Llama3 8b to solve the riddle!")
            else:
                self._move_to_room(4)
        
        elif command == "ollama list":
            print()
            self.ollama.list_models()
            print()
        
        elif command == "ollama show phi3:mini":
            print()
            self.ollama.show_model("phi3-mini")
            if not self.player.has_completed_objective("room3_inspected"):
                print("💡 The 'ollama show' command is useful for inspecting model details")
                print("before deciding whether to keep or remove them.\n")
                self.player.complete_objective("room3_inspected")
        
        elif command in ["ollama rm phi3:mini", "remove", "remove phi3", "remove phi3 mini"]:
            self._remove_phi3_mini()
        
        elif command == "ollama pull llama3:8b" or command == self.sidekicks["Llama3 8b"].summon_scroll.lower():
            self._summon_llama3()
        
        elif "ollama" in command and "pull" in command and "llama" in command:
            print("❌ Not quite right. Remember the exact command:")
            print("ollama pull llama3:8b")
        
        elif "summon" in command and "llama" in command:
            print("💡 Hint: Use the real Ollama command, not scroll text!")
            print("Try: ollama pull llama3:8b")
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            if not self.player.has_completed_objective("room3_inspected"):
                print("Hint: Try 'ollama show phi3:mini' to inspect your current model!")
            else:
                print("Hint: Use 'ollama rm phi3:mini', then 'ollama pull llama3:8b'!")
    
    def _handle_room4_commands(self, command: str) -> None:
        """Handle commands specific to Room 4 (Victory Chamber)."""
        if command == "west":
            self._move_to_room(3)
        
        elif command == "ollama apprentice":
            self._unlock_victory()
        
        elif command == "descend":
            if self.player.has_completed_objective("room4_complete"):
                self._handle_descend()
            else:
                print("\n⚠️  You must unlock the Victory Chamber first!")
                print("Hint: Enter the password revealed by Llama3 8b!")
        
        else:
            print(f"\nUnknown command. Type 'help' for available commands.")
            if not self.player.has_completed_objective("room4_complete"):
                print("Hint: Enter the password revealed by Llama3 8b!")
            else:
                print("Hint: Type 'descend' to proceed to the Tokenizer Tomb!")
    
    def _attempt_riddle_room2(self) -> None:
        """Handle riddle attempt in Room 2 with Phi3 Mini."""
        if not self.player.has_active_sidekick():
            print("⚠️  You need an active sidekick to attempt the riddle!")
            return
        
        if self.player.active_sidekick.name != "Phi3 Mini":
            print("⚠️  This is meant to be attempted with Phi3 Mini first.")
            return
        
        # Get the riddle
        riddle = self.puzzles["riddle_01"]
        
        # Have sidekick attempt it
        success, response = self.player.active_sidekick.attempt_riddle(riddle)
        print(response)
        
        # Always complete the objective after attempting (the learning is in the attempt)
        if not success:
            print("\n💡 Learning Moment:")
            print("Phi3 Mini is a small, efficient model but struggles with")
            print("certain tasks like careful counting. This is a trade-off:")
            print("smaller size = faster but less capable.")
        else:
            print("\n💡 Learning Moment:")
            print("Phi3 Mini got lucky this time! But with only a 20% success rate,")
            print("small models aren't reliable for complex tasks like precise counting.")
            print("Larger models have higher success rates for challenging problems.")
        
        # Unlock tip
        self.player.unlock_tip("tip_01", self.tips["tip_01"]["text"])
        
        # Mark objective complete
        self.player.complete_objective("room2_complete")
        self.current_room.mark_completed()
        
        print("\n✅ Objective Complete!")
        print("You've learned about the trade-offs of small models.")
        print("\nProceed east to the Upgrade Forge to get a more powerful ally!")
    
    def _remove_phi3_mini(self) -> None:
        """Remove Phi3 Mini sidekick."""
        if self.player.active_sidekick and self.player.active_sidekick.name == "Phi3 Mini":
            # Simulate ollama remove
            print("\n🗑️  Executing: ollama rm phi3:mini")
            self.ollama.remove_model("phi3-mini")
            
            # Remove from player
            message = self.player.active_sidekick.remove()
            print(message)
            self.player.set_active_sidekick(None)
            
            # Unlock tip
            self.player.unlock_tip("tip_03", self.tips["tip_03"]["text"])
            
            print("Now you can summon a more powerful model!")
            print("Type: ollama pull llama3:8b")
        else:
            print("⚠️  Phi3 Mini is not your active sidekick.")
    
    def _summon_llama3(self) -> None:
        """Summon Llama3 8b sidekick."""
        # First, simulate ollama pull
        print("\n📥 First, we need to pull the Llama3 8b model...")
        self.ollama.pull_model("llama3-8b")
        
        # Then summon
        llama3 = self.sidekicks["Llama3 8b"]
        print(llama3.summon())
        self.player.set_active_sidekick(llama3)
        
        # Mark objective complete
        self.player.complete_objective("room3_complete")
        self.current_room.mark_completed()
        
        print("\n✅ Objectives Complete!")
        print("You now have a powerful ally!")
        print("Head WEST to the Riddle Hall to retry the puzzle with greater strength!")
    
    def _run_phi3_riddle(self) -> None:
        """Handle running phi3:mini with the strawberry riddle."""
        if not self.player.has_active_sidekick():
            print("⚠️  You need to summon Phi3 Mini first!")
            print("Go back to the Summoning Chamber (west) if you haven't summoned it yet.")
            return
        
        if self.player.active_sidekick.name != "Phi3 Mini":
            print("⚠️  You don't have Phi3 Mini as your active sidekick.")
            if self.player.active_sidekick.name == "Llama3 8b":
                print("It looks like you already upgraded! Try: ollama run llama3:8b")
            return
        
        # Simulate interactive session
        print("\n🤖 Starting interactive session with phi3:mini...")
        print("Type your question, or type '/bye' to exit.\n")
        
        # Wait for user input
        user_question = input(">>> ").strip()
        
        if user_question.lower() in ["/bye", "exit", "quit"]:
            print("Exiting interactive session.\n")
            return
        
        # Check if it's about strawberry
        if "strawberry" in user_question.lower() or "r" in user_question.lower():
            # Get the riddle and have phi3 attempt it with delays
            riddle = self.puzzles["riddle_01"]
            success = self.player.active_sidekick.attempt_riddle_with_delays(riddle)
            
            print(">>> /bye")
            print("Exiting interactive session.\n")
            
            # Provide feedback
            if not success:
                print("💡 Learning Moment:")
                print("Phi3 Mini is a small, efficient model but struggles with")
                print("certain tasks like careful counting. This is a trade-off:")
                print("smaller size = faster but less capable.")
            else:
                print("💡 Learning Moment:")
                print("Phi3 Mini got lucky this time! But with only a 20% success rate,")
                print("small models aren't reliable for complex tasks like precise counting.")
                print("Larger models have higher success rates for challenging problems.")
            
            # Unlock tip
            self.player.unlock_tip("tip_01", self.tips["tip_01"]["text"])
            
            # Mark objective complete
            self.player.complete_objective("room2_complete")
            self.current_room.mark_completed()
            
            print("\n✅ Objective Complete!")
            print("You've learned about the trade-offs of small models.")
            print("\nProceed east to the Upgrade Forge to get a more powerful ally!")
        else:
            print(f"\nPhi3 Mini: That's an interesting question! However, the Oracle")
            print("is waiting for you to ask about the riddle: 'How many r's are in strawberry?'")
            print("\n>>> /bye")
            print("Exiting interactive session.\n")
    
    def _run_llama3_riddle(self) -> None:
        """Handle running llama3:8b with the strawberry riddle."""
        if not self.player.has_active_sidekick():
            print("⚠️  You need to summon a sidekick first!")
            return
        
        if self.player.active_sidekick.name != "Llama3 8b":
            print("⚠️  You don't have Llama3 8b as your active sidekick.")
            if self.player.active_sidekick.name == "Phi3 Mini":
                print("You need to upgrade first. Go east to the Upgrade Forge!")
            return
        
        # Simulate interactive session
        print("\n🤖 Starting interactive session with llama3:8b...")
        print("Type your question, or type '/bye' to exit.\n")
        
        # Wait for user input
        user_question = input(">>> ").strip()
        
        if user_question.lower() in ["/bye", "exit", "quit"]:
            print("Exiting interactive session.\n")
            return
        
        # Check if it's about strawberry
        if "strawberry" in user_question.lower() or "r" in user_question.lower():
            # Get the riddle and have llama3 attempt it (should succeed)
            riddle = self.puzzles["riddle_01"]
            success = self.player.active_sidekick.attempt_riddle_with_delays(riddle)
            
            if success:
                print("The Oracle's eyes glow with approval!")
                print("\n✨ The treasure chest begins to glow with golden light! ✨")
                print("Ancient locks click open one by one...")
                print("The chest lid slowly rises, revealing a scroll inside.")
                print("\nLlama3 8b continues: 'By the way, you've earned access to the Victory Chamber.'")
                # Display password in cross-platform ASCII box
                print("\nThe Oracle reveals:")
                print("╔════════════════════════════════════╗")
                print("║   PASSWORD: Ollama Apprentice     ║")
                print("╚════════════════════════════════════╝")
                print("\n>>> /bye")
                print("Exiting interactive session.\n")
                
                # Unlock tip
                self.player.unlock_tip("tip_02", self.tips["tip_02"]["text"])
                
                # Mark that password is discovered
                self.player.discover_password()
                
                print("🔑 Password discovered! You can now proceed to the Victory Chamber.")
                print("Head EAST through the Forge to reach the Victory Chamber!")
            else:
                print("\n>>> /bye")
                print("Exiting interactive session.\n")
                print("(Rare case: Even large models can occasionally fail. Try again!)")
        else:
            print(f"\nLlama3 8b: That's an interesting question! However, the Oracle")
            print("is waiting for you to ask about the riddle: 'How many r's are in strawberry?'")
            print("\n>>> /bye")
            print("Exiting interactive session.\n")
    
    def _attempt_riddle_room4(self) -> None:
        """Handle riddle attempt in Room 4 with Llama3 8b."""
        if not self.player.has_active_sidekick():
            print("⚠️  You need an active sidekick to attempt the riddle!")
            return
        
        if self.player.active_sidekick.name != "Llama3 8b":
            print("⚠️  You should use Llama3 8b for this challenge.")
            return
        
        # Get the riddle
        riddle = self.puzzles["riddle_01"]
        
        # Have sidekick attempt it
        success, response = self.player.active_sidekick.attempt_riddle(riddle)
        print(response)
        
        if success:
            print("\n🎉 VICTORY! 🎉")
            print("Llama3 8b successfully solved the riddle!")
            
            # Unlock tip
            self.player.unlock_tip("tip_02", self.tips["tip_02"]["text"])
            
            # Award points
            self.player.add_knowledge_points(100)
            
            # Mark complete
            self.player.complete_objective("room4_complete")
            self.current_room.mark_completed()
            
            # Show victory screen
            print()
            display_victory()
            
            print("🏆 GROUND LEVEL COMPLETE! 🏆\n")
            print(f"Final Knowledge Points: {self.player.knowledge_points}")
            print(f"Tips Unlocked: {len(self.player.unlocked_tips)}/4")
            
            self.player.display_unlocked_tips(self.tips)
            
            print("\n" + "="*60)
            print("Thank you for playing AI-LLM-Dungeon: Ground Level!")
            print("You've learned the fundamentals of Ollama and LLM management.")
            print("="*60 + "\n")
            
            # Enable post-victory exploration
            print("🌟 POST-VICTORY EXPLORATION ENABLED! 🌟")
            print("\nYou can now freely explore the dungeon to review your learnings!")
            print("Move between rooms using 'east' and 'west' commands.")
            print("Visit any room to revisit what you learned:")
            print("  • Room 0 (west): Ollama Village - Review basic commands")
            print("  • Room 1 (west): Summoning Chamber - Model pulling")
            print("  • Room 2 (west): Riddle Hall - Model capabilities")
            print("  • Room 3 (west): Upgrade Forge - Model management")
            print("  • Room 4: Victory Chamber (you are here)")
            print("\nType 'quit' when you're ready to exit.\n")
            
            # DO NOT set game_running to False - allow exploration!
            # self.game_running = False  <-- Removed this line
        else:
            print("\n(Rare case: Even large models can occasionally fail.)")
            print("Try 'riddle' again!")
    
    def _unlock_victory(self) -> None:
        """Handle password entry to unlock the Victory Chamber."""
        print("\n🔓 Password accepted!")
        print("The ancient lock glows brightly and the chamber doors swing open!")
        print("\nYou step inside the Victory Chamber...")
        time.sleep(1.5)
        print()
        
        # Award points
        self.player.add_knowledge_points(100)
        
        # Mark complete
        self.player.complete_objective("room4_complete")
        self.current_room.mark_completed()
        
        # Show victory screen
        display_victory()
        time.sleep(1.0)
        
        print("🏆 GROUND LEVEL COMPLETE! 🏆\n")
        print("You have earned the title: \"Ollama Apprentice\"\n")
        time.sleep(1.0)
        
        # Display certificate
        display_certificate()
        time.sleep(1.5)
        
        # Prompt user to press Enter before showing the path forward
        print()
        input("Press Enter to continue...")
        print()
        
        # Show the path forward
        print("\n🚪 THE PATH FORWARD 🚪\n")
        print("Your training is complete, but your adventure has just begun!")
        print("The dungeon descends deeper with greater challenges awaiting...\n")
        time.sleep(1.0)
        
        print("  ⬇️  NEXT: Token Crypts")
        print("      Learn how LLMs see the world through tokens.")
        print("      Run: python3 ./token_crypts_cli.py\n")
        time.sleep(0.8)
        
        print("  🔮 COMING SOON:")
        print("      • Temperature Tavern - Master sampling parameters")
        print("      • Context Catacombs - Understand context windows")
        print("      • Prompt Palace - Advanced prompt engineering\n")
        time.sleep(0.8)
        
        # Real-world next steps
        print("💡 REAL-WORLD NEXT STEPS:")
        print("   1. Install Ollama: https://ollama.com/download")
        print("   2. Pull your first model: ollama pull llama3")
        print("   3. Start chatting: ollama run llama3")
        print()
        print("📚 Learn more about Ollama:")
        print("   • GitHub repository: https://github.com/ollama/ollama")
        print("   • API docs: https://github.com/ollama/ollama/blob/main/docs/api.md")
        print("   • Model library: https://ollama.com/library\n")
        time.sleep(0.5)
        
        # Show stats
        print(f"Final Knowledge Points: {self.player.knowledge_points}")
        print(f"Tips Unlocked: {len(self.player.unlocked_tips)}/4\n")
        
        self.player.display_unlocked_tips(self.tips)
        
        # Enable exploration and descend option
        print("\n" + "="*60)
        print("Type 'descend' to proceed to deeper levels, or 'quit' to exit.")
        print("You can also explore the dungeon by moving 'west' to revisit rooms.")
        print("="*60 + "\n")
    
    def _handle_descend(self) -> None:
        """Handle the descend command to transition to deeper levels."""
        print()
        display_descend()
        print()
        
        slow_print("You approach the ancient stone staircase at the back of the Victory Chamber.")
        slow_print("The air grows cooler as you peer into the darkness below...")
        slow_print("Carved into the archway above the stairs, you read:")
        slow_print("  'Deeper knowledge awaits those who dare to descend'\n")
        
        slow_print("You've mastered the fundamentals of Ollama.")
        slow_print("Now it's time to learn how LLMs truly see the world.\n")
        
        # Use the shared navigation system
        show_descend_menu("Ground Level (Ollama Village)")
    
    def _move_to_room(self, room_id: int) -> None:
        """
        Move the player to a different room.
        
        Args:
            room_id: ID of the room to move to
        """
        can_proceed, reason = self.player.can_proceed_to_room(room_id)
        
        if not can_proceed:
            print(f"⚠️  {reason}")
            return
        
        # Move player
        self.player.move_to_room(room_id)
        self.current_room = create_room(room_id)
        
        # Show transition
        display_room_transition()
        
        # Enter new room
        self.current_room.enter(self.player)
    
    def _handle_quit(self) -> None:
        """Handle quit command."""
        print("\nThank you for playing AI-LLM-Dungeon!")
        print("\n💡 To continue your adventure later:")
        print("   • Run this level again: python3 ./ground_level_cli.py")
        print("   • Try other levels: python3 ./token_crypts_cli.py")
        print("   • Use 'ls' to see all available level scripts")
        print("\nYour progress has been noted. Farewell, adventurer!\n")
        self.game_running = False
    
    def _handle_help(self) -> None:
        """Display help information."""
        level_specific = """LEARNING:
  learn                    - Begin or continue lessons with the Shaman
  tips                     - View unlocked knowledge tips

OLLAMA COMMANDS (as you learn them):
  ollama                   - Base ollama command
  ollama serve             - Start ollama server
  ollama list              - List installed models
  ollama pull <model>      - Download a model
  ollama run <model>       - Run/chat with a model
  ollama show <model>      - Show model information
  ollama rm <model>        - Remove a model

ROOM-SPECIFIC:
  summon <model>           - Summon sidekick in Summoning Chamber
  answer <text>            - Answer riddles in Riddle Hall
  upgrade <sidekick>       - Upgrade sidekick in Upgrade Forge"""
        
        tips = """TIPS:
  - Follow the Shaman's teachings in Ollama Village
  - Room-specific commands vary - follow the prompts!
  - Use 'east' or 'west' to move between rooms when available"""
        
        print(self.standard_commands.format_help(level_specific, tips))
    
    def _handle_status(self) -> None:
        """Display player status."""
        print(self.player.get_status())
        
        if self.player.active_sidekick:
            print("ACTIVE SIDEKICK:")
            print(self.player.active_sidekick.get_status())
    
    def _handle_tips(self) -> None:
        """Display unlocked tips."""
        self.player.display_unlocked_tips(self.tips)
    
    def _handle_look(self) -> None:
        """Display current room description."""
        if self.current_room:
            print(f"\n{self.current_room.get_description()}\n")
        else:
            print("You are nowhere.")
    
    def _handle_ls(self) -> None:
        """List available exits from current room."""
        room_id = self.player.current_room
        
        # Define room connections
        exits = {}
        if room_id == 0:
            if self.player.has_completed_objective("room0_complete"):
                exits = {"east": "Summoning Chamber"}
        elif room_id == 1:
            exits = {"west": "Ollama Village"}
            if self.player.active_sidekick:
                exits["east"] = "Riddle Hall"
        elif room_id == 2:
            exits = {"west": "Summoning Chamber"}
            if self.player.has_completed_objective("room2_complete"):
                exits["east"] = "Upgrade Forge"
        elif room_id == 3:
            exits = {"west": "Riddle Hall"}
            if self.player.has_completed_objective("room3_complete"):
                exits["east"] = "Victory Chamber"
        elif room_id == 4:
            exits = {"west": "Upgrade Forge"}
        
        if not exits:
            print("\nNo exits available from this room yet.\n")
            return
        
        print("\nAvailable directions:")
        for direction, destination in exits.items():
            print(f"  {direction} -> {destination}")
        print()
    
    def _handle_pwd(self) -> None:
        """Show ASCII map with current position marked."""
        room_id = self.player.current_room
        
        # Map room IDs to display labels
        room_map = {
            0: "VILLAGE",
            1: "SUMMON",
            2: "RIDDLE",
            3: "FORGE",
            4: "VICTORY"
        }
        
        # ASCII map layout
        map_layout = [
            "    [VILLAGE]───[SUMMON]───[RIDDLE]───[FORGE]───[VICTORY]"
        ]
        
        # Mark current position
        print()
        for line in map_layout:
            output_line = line
            for rid, label in room_map.items():
                if rid == room_id:
                    output_line = output_line.replace(f"[{label}]", f"[{label}*]")
            print(output_line)
        print()
    
    def _handle_map(self) -> None:
        """Display full level map."""
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                      OLLAMA VILLAGE MAP                      ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print("    [VILLAGE]───[SUMMON]───[RIDDLE]───[FORGE]───[VICTORY]")
        print()
        print("  • VILLAGE     - Ollama Village (Learn Ollama basics)")
        print("  • SUMMON      - Summoning Chamber (Summon your sidekick)")
        print("  • RIDDLE      - Riddle Hall (Solve riddles with your sidekick)")
        print("  • FORGE       - Upgrade Forge (Upgrade your sidekick)")
        print("  • VICTORY     - Victory Chamber (Complete the level)")
        print()
