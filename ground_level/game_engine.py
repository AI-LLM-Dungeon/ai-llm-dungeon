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
        
        # Initialize first room
        self.current_room = create_room(1)
    
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
    
    def _handle_room1_commands(self, command: str) -> None:
        """Handle commands specific to Room 1 (Summoning Chamber)."""
        # Check for exact scroll text
        phi3 = self.sidekicks["Phi3 Mini"]
        
        if command == phi3.summon_scroll.lower():
            # Correct summon command!
            print(phi3.summon())
            self.player.set_active_sidekick(phi3)
            
            # Unlock tip
            self.player.unlock_tip("tip_04", self.tips["tip_04"]["text"])
            
            # Mark objective complete
            self.player.complete_objective("room1_complete")
            self.current_room.mark_completed()
            
            print("\n✅ Objective Complete!")
            print("You've learned to summon a sidekick with the correct scroll text.")
            print("\nYou can now proceed to the next room.")
            print("Type 'east' to continue your journey.")
        
        elif command == "east":
            if self.player.has_completed_objective("room1_complete"):
                self._move_to_room(2)
            else:
                print("⚠️  You must complete this room's objectives first!")
                print("Try summoning Phi3 Mini using the scroll text.")
        
        elif "summon" in command:
            print("❌ That's not quite right.")
            print("You must type the EXACT text from the scroll to summon.")
            print("Look at the scroll and type exactly what it says.")
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: Try typing the exact text from the scroll!")
    
    def _handle_room2_commands(self, command: str) -> None:
        """Handle commands specific to Room 2 (Riddle Hall)."""
        if command == "west":
            self._move_to_room(1)
        
        elif command == "east":
            if self.player.has_completed_objective("room2_complete"):
                self._move_to_room(3)
            else:
                print("⚠️  You must complete this room's objectives first!")
        
        elif command in ["riddle", "attempt", "try riddle", "solve"]:
            self._attempt_riddle_room2()
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: Try 'riddle' to have your sidekick attempt the puzzle!")
    
    def _handle_room3_commands(self, command: str) -> None:
        """Handle commands specific to Room 3 (Upgrade Forge)."""
        if command == "west":
            self._move_to_room(2)
        
        elif command == "east":
            if self.player.has_completed_objective("room3_complete"):
                self._move_to_room(4)
            else:
                print("⚠️  You must complete this room's objectives first!")
        
        elif command in ["remove", "remove phi3", "remove phi3 mini"]:
            self._remove_phi3_mini()
        
        elif command == self.sidekicks["Llama3 8b"].summon_scroll.lower():
            self._summon_llama3()
        
        elif "summon" in command and "llama" in command:
            llama_scroll = self.sidekicks["Llama3 8b"].summon_scroll
            print("❌ Not quite right. Remember the exact scroll text:")
            print(f"'{llama_scroll}'")
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: First 'remove' Phi3 Mini, then summon Llama3 8b!")
    
    def _handle_room4_commands(self, command: str) -> None:
        """Handle commands specific to Room 4 (Victory Chamber)."""
        if command == "west":
            self._move_to_room(3)
        
        elif command in ["riddle", "attempt", "try riddle", "solve"]:
            self._attempt_riddle_room4()
        
        else:
            print(f"Unknown command. Type 'help' for available commands.")
            print("Hint: Try 'riddle' to have Llama3 8b attempt the puzzle!")
    
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
            self.ollama.remove_model("phi3-mini")
            
            # Remove from player
            message = self.player.active_sidekick.remove()
            print(message)
            self.player.set_active_sidekick(None)
            
            # Unlock tip
            self.player.unlock_tip("tip_03", self.tips["tip_03"]["text"])
            
            llama_scroll = self.sidekicks["Llama3 8b"].summon_scroll
            print("Now you can summon a more powerful model!")
            print(f"Type: '{llama_scroll}'")
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
        print("You now have a powerful ally! Head east to retry the riddle.")
    
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
            
            self.game_running = False
        else:
            print("\n(Rare case: Even large models can occasionally fail.)")
            print("Try 'riddle' again!")
    
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
