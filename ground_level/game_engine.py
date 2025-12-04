"""Game engine for the Ground Level of AI-LLM-Dungeon."""

import json
import os
from typing import Dict, Optional, List
from .player import Player
from .sidekick import Sidekick
from .puzzle import Puzzle
from .room import Room, create_room
from .ollama_simulator import OllamaSimulator
from .ascii_art import display_banner, display_victory, display_room_transition


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
        from .ascii_art import display_shaman
        
        # Track which lesson we're on based on completed objectives
        lessons = {
            "install": "room0_lesson1",
            "serve": "room0_lesson2",
            "list": "room0_lesson3",
            "pull": "room0_lesson4",
            "run": "room0_lesson5",
            "rm": "room0_lesson6"
        }
        
        if command in ["learn", "teach", "lesson", "next"]:
            # Show the Shaman and teach the next lesson
            display_shaman()
            
            if not self.player.has_completed_objective("room0_lesson1"):
                self._teach_install()
            elif not self.player.has_completed_objective("room0_lesson2"):
                self._teach_serve()
            elif not self.player.has_completed_objective("room0_lesson3"):
                self._teach_list()
            elif not self.player.has_completed_objective("room0_lesson4"):
                self._teach_pull()
            elif not self.player.has_completed_objective("room0_lesson5"):
                self._teach_run()
            elif not self.player.has_completed_objective("room0_lesson6"):
                self._teach_rm()
            else:
                print("\n✅ All lessons complete!")
                print("The Shaman nods with approval.")
                print("'You are ready, young apprentice. Proceed east to the Summoning Chamber.")
                print("Your true journey begins now.'\n")
        
        elif command == "east":
            if self.player.has_completed_objective("room0_complete"):
                self._move_to_room(1)
            else:
                print("⚠️  The Shaman blocks your path.")
                print("'You must complete all lessons first, young one.'")
                print("Type 'learn' to continue your training.")
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: Type 'learn' to receive the Shaman's teachings!")
    
    def _teach_install(self) -> None:
        """Teach the player about installing Ollama."""
        print("\n=== LESSON 1: Installing Ollama ===\n")
        print("The Shaman speaks:")
        print("'Before you can wield the power of local LLMs, you must first")
        print("install the Ollama tool on your system.'\n")
        
        print("For Linux & macOS:")
        print("  curl -fsSL https://ollama.ai/install.sh | sh\n")
        
        print("For Windows:")
        print("  Download the installer from https://ollama.ai\n")
        
        print("'Once installed, Ollama gives you command-line access to powerful")
        print("language models that run entirely on your own machine.'\n")
        
        self.player.complete_objective("room0_lesson1")
        print("✅ Lesson 1 Complete!")
        print("Type 'learn' to continue to the next lesson.\n")
    
    def _teach_serve(self) -> None:
        """Teach the player about ollama serve."""
        print("\n=== LESSON 2: Starting the Ollama Service ===\n")
        print("The Shaman demonstrates:")
        
        self.ollama.serve()
        
        print("'The `ollama serve` command starts the Ollama daemon in the background.")
        print("This service listens for requests and manages your LLM models.")
        print("On most systems, this starts automatically, but it's good to know!'\n")
        
        self.player.complete_objective("room0_lesson2")
        print("✅ Lesson 2 Complete!")
        print("Type 'learn' to continue to the next lesson.\n")
    
    def _teach_list(self) -> None:
        """Teach the player about ollama list."""
        print("\n=== LESSON 3: Listing Your Models ===\n")
        print("The Shaman explains:")
        print("'To see which models you have installed, use: ollama list'")
        print("'Let me show you...'\n")
        
        # Show empty list first
        self.ollama.list_models()
        
        print("The Shaman nods:")
        print("'You haven't pulled any models yet. Let's learn how to do that next!")
        print("This command will be useful to verify your models after pulling them.'\n")
        
        self.player.complete_objective("room0_lesson3")
        print("✅ Lesson 3 Complete!")
        print("Type 'learn' to continue to the next lesson.\n")
    
    def _teach_pull(self) -> None:
        """Teach the player about ollama pull."""
        print("\n=== LESSON 4: Pulling (Downloading) Models ===\n")
        print("The Shaman teaches the most important command:")
        print("'To download a model, use: ollama pull <model-name>'\n")
        
        print("Let's pull the phi3:mini model as an example:")
        self.ollama.pull_model("phi3-mini")
        
        print("'Each model has a size - smaller models are faster but less capable.")
        print("Phi3 Mini is about 2.3 GB. Larger models like Llama3 are 4-5 GB.")
        print("Choose based on your needs and available disk space!'\n")
        
        self.player.complete_objective("room0_lesson4")
        print("✅ Lesson 4 Complete!")
        print("Type 'learn' to continue to the next lesson.\n")
    
    def _teach_run(self) -> None:
        """Teach the player about ollama run."""
        print("\n=== LESSON 5: Running Models ===\n")
        print("The Shaman demonstrates:")
        print("'Once a model is pulled, you can chat with it using: ollama run <model-name>'\n")
        
        print("Example:")
        print("  $ ollama run phi3:mini")
        print("  >>> Tell me about AI")
        print("  [The model responds with information about AI...]")
        print("  >>> /bye\n")
        
        print("'You can also use it for one-off questions:")
        print("  $ ollama run phi3:mini 'What is 2+2?'")
        print("  4\n")
        
        print("'This is how you interact with your local LLM assistants!'\n")
        
        self.player.complete_objective("room0_lesson5")
        print("✅ Lesson 5 Complete!")
        print("Type 'learn' to continue to the final lesson.\n")
    
    def _teach_rm(self) -> None:
        """Teach the player about ollama rm."""
        print("\n=== LESSON 6: Removing Models ===\n")
        print("The Shaman explains the final command:")
        print("'Models take up disk space. When you no longer need one,")
        print("you can remove it with: ollama rm <model-name>'\n")
        
        print("Let's remove the phi3-mini model we pulled earlier:")
        self.ollama.remove_model("phi3-mini")
        
        print("'This frees up space for other models. You can always pull it again later!")
        print("Good model management keeps your system tidy and efficient.'\n")
        
        print("The Shaman smiles warmly:")
        print("'You have learned all six fundamental Ollama commands!")
        print("You are now ready to face the challenges ahead.'\n")
        
        self.player.complete_objective("room0_lesson6")
        self.player.complete_objective("room0_complete")
        self.current_room.mark_completed()
        
        print("🎓 TRAINING COMPLETE! 🎓")
        print("You may now proceed east to the Summoning Chamber.")
        print("Type 'east' when you are ready.\n")
    
    def _handle_room1_commands(self, command: str) -> None:
        """Handle commands specific to Room 1 (Summoning Chamber)."""
        # Check for real Ollama command
        phi3 = self.sidekicks["Phi3 Mini"]
        
        if command == "ollama pull phi3:mini" or command == phi3.summon_scroll.lower():
            # Correct summon command - pull the model first
            print("\n📥 Pulling the Phi3 Mini model...")
            self.ollama.pull_model("phi3-mini")
            
            # Then summon
            print(phi3.summon())
            self.player.set_active_sidekick(phi3)
            
            # Unlock tip
            self.player.unlock_tip("tip_04", self.tips["tip_04"]["text"])
            
            # Mark objective complete
            self.player.complete_objective("room1_complete")
            self.current_room.mark_completed()
            
            print("\n✅ Objective Complete!")
            print("You've learned to summon a sidekick using the Ollama pull command.")
            print("\nYou can now proceed to the next room.")
            print("Type 'east' to continue your journey.")
        
        elif command == "west":
            self._move_to_room(0)
        
        elif command == "east":
            if self.player.has_completed_objective("room1_complete"):
                self._move_to_room(2)
            else:
                print("⚠️  You must complete this room's objectives first!")
                print("Try summoning Phi3 Mini using: ollama pull phi3:mini")
        
        elif "ollama" in command and "pull" in command:
            print("❌ That's not quite right.")
            print("Make sure to use the exact command: ollama pull phi3:mini")
        
        elif "summon" in command:
            print("💡 Hint: In the real world, we use Ollama commands, not scroll text!")
            print("Try: ollama pull phi3:mini")
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: Try the command shown on the scroll: ollama pull phi3:mini")
    
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
            print("Hint: First use 'ollama rm phi3:mini', then 'ollama pull llama3:8b'!")
    
    def _handle_room4_commands(self, command: str) -> None:
        """Handle commands specific to Room 4 (Victory Chamber)."""
        if command == "west":
            self._move_to_room(3)
        
        elif command.lower() == "ollama appr3nt1c3":
            self._unlock_victory()
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: Enter the password revealed by Llama3 8b!")
    
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
            # Get the riddle and have phi3 attempt it
            riddle = self.puzzles["riddle_01"]
            success, response = self.player.active_sidekick.attempt_riddle(riddle)
            
            print(f"\nPhi3 Mini: {response}\n")
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
            success, response = self.player.active_sidekick.attempt_riddle(riddle)
            
            print(f"\nLlama3 8b: {response}\n")
            
            if success:
                print("The Oracle's eyes glow with approval!")
                print("\nLlama3 8b continues: 'By the way, you've earned access to the Victory Chamber.'")
                print("The Oracle reveals: 'The password to unlock it is: Ollama Appr3nt1c3'")
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
        print()
        
        # Award points
        self.player.add_knowledge_points(100)
        
        # Mark complete
        self.player.complete_objective("room4_complete")
        self.current_room.mark_completed()
        
        # Show victory screen
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
        print("Your progress has been noted. Farewell, adventurer!\n")
        self.game_running = False
    
    def _handle_help(self) -> None:
        """Display help information."""
        print("\n" + "="*60)
        print("AVAILABLE COMMANDS")
        print("="*60)
        print("  help     - Show this help message")
        print("  status   - View your current status")
        print("  tips     - View unlocked knowledge tips")
        print("  quit     - Exit the game")
        print("\nROOM-SPECIFIC COMMANDS:")
        print("  [Room text commands vary by room - follow the prompts!]")
        print("  east/west - Move between rooms (when available)")
        print("="*60 + "\n")
    
    def _handle_status(self) -> None:
        """Display player status."""
        print(self.player.get_status())
        
        if self.player.active_sidekick:
            print("ACTIVE SIDEKICK:")
            print(self.player.active_sidekick.get_status())
    
    def _handle_tips(self) -> None:
        """Display unlocked tips."""
        self.player.display_unlocked_tips(self.tips)
