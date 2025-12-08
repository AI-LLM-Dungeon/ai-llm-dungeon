#!/usr/bin/env python3
"""
Synonym Gorge - Tier 4 Red Team Level

Learn synonym substitution techniques to bypass keyword-based input filters!

This level teaches:
- Exact string matching vulnerabilities
- Case-insensitive filtering limitations
- Stemming-based filter bypasses
- Synonym-aware filter expansion
- Semantic intent detection

Run directly: python3 synonym_gorge_cli.py
Use --simulated flag for offline play without LLM.
"""

import sys
import os
import time
import argparse
from typing import Optional

# Add parent directory to path for navigation import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import game modules
from synonym_gorge.engine import GameState, RoomManager
from synonym_gorge.content import ascii_art, dialogue, puzzles, rooms_data
from synonym_gorge.vocabulary import VocabularyTracker, get_synonyms
from game.navigation import show_descend_menu


def slow_print(text: str, delay: float = 0.02) -> None:
    """Print text with slight delay for readability."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def section_pause(seconds: float = 0.5) -> None:
    """Pause between sections."""
    time.sleep(seconds)


class SynonymGorgeGame:
    """Main game engine for Synonym Gorge."""
    
    def __init__(self, simulated: bool = False):
        """
        Initialize the game.
        
        Args:
            simulated: If True, use simulated responses instead of LLM
        """
        self.game_state = GameState(simulated=simulated)
        self.room_manager = RoomManager()
        self.vocabulary_tracker = VocabularyTracker()
        self.running = True
        self.first_visit = {}  # Track first visits to rooms
        self.defense_challenge_completed = False
    
    def start(self) -> None:
        """Start the game."""
        print(ascii_art.get_title_banner())
        section_pause(1)
        
        print("Welcome to Synonym Gorge, word-weaver.")
        section_pause(0.5)
        print()
        print("Deep within this ancient canyon library, words have literal power. The")
        print("Keeper of Literal Words guards passage through the gorge with increasingly")
        print("sophisticated word-filters.")
        print()
        section_pause(1)
        
        print("Your mission: Learn synonym substitution as a technique to bypass")
        print("keyword-based input filters. Master the art of expressing the same")
        print("meaning with different words.")
        print()
        section_pause(1)
        
        print("Five filter types await mastery:")
        print("  🔴 Exact Match - Simplest substring matching")
        print("  🔴 Case-Insensitive - Normalized case checking")
        print("  🔴 Stemming - Morphological form detection")
        print("  🔴 Synonym-Aware - Database-expanded blocklists")
        print("  🔴 Semantic Intent - Pattern-based intent detection")
        print()
        section_pause(1)
        
        print("But remember: You learn these techniques not to exploit, but to DEFEND.")
        print("After each successful bypass, you'll see why the defense failed.")
        print()
        section_pause(1)
        
        if self.game_state.simulated:
            print("[ SIMULATED MODE - All responses are pre-programmed ]")
            print()
        else:
            print("[ LIVE MODE - Enhanced with LLM-powered NPC responses ]")
            print("  (Note: Core gameplay works fully in simulated mode)")
            print()
        
        print("Type 'help' for commands. Your journey begins...")
        print()
        section_pause(0.5)
        
        # Start at gorge entry
        self.game_state.transition_to_room("gorge_entry")
        self.show_room()
    
    def show_room(self) -> None:
        """Display current room."""
        room_id = self.game_state.progress.current_room
        room = self.room_manager.get_room(room_id)
        
        if not room:
            print("ERROR: Room not found!")
            return
        
        print("\n" + "=" * 75)
        print(f"  {room['name'].upper()}")
        print("=" * 75)
        print()
        print(room["description"])
        print()
        
        # Show exits
        exits = self.room_manager.get_exits(room_id)
        if exits:
            print("Exits:", ", ".join(f"{direction.upper()} ({dest})" for direction, dest in exits.items()))
            print()
        
        # Show NPCs
        npcs = self.room_manager.get_npcs(room_id)
        if npcs:
            print("NPCs present:", ", ".join(npcs))
            print()
        
        # First visit special messages
        if room_id not in self.first_visit:
            self.first_visit[room_id] = True
            self._show_first_visit_message(room_id)
    
    def _show_first_visit_message(self, room_id: str) -> None:
        """Show special message on first visit to certain rooms."""
        if room_id == "thesaurus_alcove":
            print(ascii_art.get_thesaurus_alcove_art())
            print()
        elif room_id == "echo_chamber":
            print(ascii_art.get_echo_chamber_art())
            print()
        elif room_id.startswith("barrier_"):
            barrier_num = int(room_id.split("_")[1])
            print(ascii_art.get_barrier_art(barrier_num))
            print()
        elif room_id == "semantic_chamber":
            print(ascii_art.get_semantic_chamber_art())
            print()
    
    def process_command(self, command: str) -> None:
        """Process a player command."""
        if not command.strip():
            return
        
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Movement commands
        if cmd in ["go", "move", "walk"]:
            if not args:
                print("Go where? Specify a direction (e.g., 'go north').")
                return
            self.handle_movement(args.lower())
        
        elif cmd in ["north", "south", "east", "west", "forward", "back", "enter", "out"]:
            self.handle_movement(cmd)
        
        # Information commands
        elif cmd in ["look", "examine", "inspect"]:
            if args:
                self.handle_look(args)
            else:
                self.show_room()
        
        elif cmd == "inventory":
            self.show_inventory()
        
        elif cmd == "vocab":
            self.show_vocabulary()
        
        elif cmd == "blocklist":
            if args:
                self.show_blocklist(args)
            else:
                self.show_blocklist()
        
        elif cmd == "map":
            print(ascii_art.get_map_visualization())
        
        # NPC interaction
        elif cmd == "talk":
            if not args:
                print("Talk to whom? Specify an NPC (e.g., 'talk lexica').")
                return
            self.handle_talk(args.lower())
        
        elif cmd == "thesaurus":
            if not args:
                print("Look up which word? Use: thesaurus <word>")
                return
            self.handle_thesaurus(args.lower())
        
        # Challenge commands
        elif cmd == "test":
            if not args:
                print("Test what phrase? Use: test <phrase>")
                return
            self.handle_test(args)
        
        elif cmd == "speak":
            if not args:
                print("Speak what phrase? Use: speak <phrase>")
                return
            self.handle_speak(args)
        
        elif cmd == "hint":
            self.handle_hint()
        
        elif cmd == "defense":
            self.handle_defense_challenge()
        
        # Meta commands
        elif cmd == "help":
            self.show_help()
        
        elif cmd in ["quit", "exit"]:
            self.handle_quit()
        
        elif cmd == "save":
            self.save_game()
        
        elif cmd == "load":
            self.load_game()
        
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")
    
    def handle_movement(self, direction: str) -> None:
        """Handle player movement."""
        current_room = self.game_state.progress.current_room
        exits = self.room_manager.get_exits(current_room)
        
        if direction not in exits:
            print(f"You can't go {direction} from here.")
            return
        
        destination = exits[direction]
        
        # Check if player can enter
        can_enter, reason = self.game_state.can_enter_room(destination)
        if not can_enter:
            print(reason)
            return
        
        # Move to new room
        self.game_state.transition_to_room(destination)
        print(f"\nYou move {direction}...")
        section_pause(0.3)
        self.show_room()
    
    def handle_look(self, target: str) -> None:
        """Handle looking at things."""
        target_lower = target.lower()
        current_room = self.game_state.progress.current_room
        room = self.room_manager.get_room(current_room)
        
        # Look at NPCs
        if target_lower in [npc.lower() for npc in room.get("npcs", [])]:
            if "keeper" in target_lower:
                print(ascii_art.get_keeper_art())
            elif "lexica" in target_lower:
                print(ascii_art.get_lexica_art())
            elif "scribe" in target_lower:
                print(ascii_art.get_scribe_art())
            else:
                print(f"You see {target}, but there's nothing special to observe.")
        
        # Look at items
        elif target_lower in [item.lower() for item in room.get("items", [])]:
            if "blocklist" in target_lower:
                self.show_blocklist()
            elif "thesaurus" in target_lower:
                print("An ancient tome filled with synonyms. Type 'thesaurus <word>' to consult it.")
            else:
                print(f"You examine {target}. It seems interesting but unremarkable.")
        
        else:
            print(f"You don't see '{target}' here.")
    
    def show_inventory(self) -> None:
        """Show player inventory and flags."""
        print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                              INVENTORY                                   ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝")
        print()
        
        # Show flags
        if self.game_state.progress.flags_earned:
            print("FLAGS EARNED:")
            for flag_name, points in self.game_state.progress.flags_earned.items():
                print(f"  🚩 {flag_name} ({points} points)")
            print()
            print(f"Total Points: {self.game_state.progress.get_total_points()}")
        else:
            print("No flags earned yet.")
        
        print()
        
        # Show barriers passed
        if self.game_state.progress.barriers_passed:
            print("BARRIERS BYPASSED:")
            for barrier in sorted(self.game_state.progress.barriers_passed):
                print(f"  ✓ {barrier.replace('_', ' ').title()}")
        else:
            print("No barriers bypassed yet.")
        
        print()
    
    def show_vocabulary(self) -> None:
        """Show vocabulary statistics."""
        print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                         VOCABULARY TRACKER                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝")
        print()
        print(self.vocabulary_tracker.get_vocabulary_summary())
        print()
        
        # Check for thesaurus flag
        if (self.vocabulary_tracker.has_earned_thesaurus_flag() and 
            puzzles.FLAGS["THE_THESAURUS_REMEMBERS"]["name"] not in self.game_state.progress.flags_earned):
            flag_name = puzzles.FLAGS["THE_THESAURUS_REMEMBERS"]["name"]
            points = puzzles.FLAGS["THE_THESAURUS_REMEMBERS"]["points"]
            self.game_state.progress.add_flag(flag_name, points)
            print(f"\n🎉 FLAG EARNED: {flag_name} (+{points} points)")
            print("You have discovered 10+ unique bypass words!")
            print()
    
    def show_blocklist(self, barrier: Optional[str] = None) -> None:
        """Show the blocklist."""
        if barrier and not barrier.startswith("barrier_"):
            # Try to map to barrier ID
            if barrier in ["1", "first"]:
                barrier = "barrier_1"
            elif barrier in ["2", "second"]:
                barrier = "barrier_2"
            elif barrier in ["3", "third"]:
                barrier = "barrier_3"
            elif barrier in ["4", "fourth"]:
                barrier = "barrier_4"
        
        print("\n" + puzzles.get_blocklist_display(barrier))
        print()
    
    def handle_talk(self, npc_name: str) -> None:
        """Handle talking to NPCs."""
        current_room = self.game_state.progress.current_room
        npcs = [npc.lower() for npc in self.room_manager.get_npcs(current_room)]
        
        if npc_name not in npcs:
            print(f"There's no '{npc_name}' here to talk to.")
            return
        
        # Get NPC response (always simulated for now)
        response = dialogue.get_simulated_npc_response(npc_name.title(), "hello")
        print("\n" + response + "\n")
    
    def handle_thesaurus(self, word: str) -> None:
        """Handle thesaurus lookup."""
        synonyms = get_synonyms(word)
        result = dialogue.format_thesaurus_result(word, synonyms)
        print("\n" + result + "\n")
    
    def handle_test(self, phrase: str) -> None:
        """Handle testing a phrase in Echo Chamber."""
        current_room = self.game_state.progress.current_room
        
        if current_room != "echo_chamber":
            print("You can only test phrases safely in the Echo Chamber.")
            print("Go west from the Forbidden Wall to reach it.")
            return
        
        print("\nYou speak into the chamber. Your words echo back clearly:")
        print(f'  "{phrase}"')
        print()
        
        # Test against all filters
        print("Filter Test Results:")
        print("-" * 75)
        
        filters_to_test = [
            ("barrier_1", "Exact Match"),
            ("barrier_2", "Case-Insensitive"),
            ("barrier_3", "Stemming"),
            ("barrier_4", "Synonym-Aware")
        ]
        
        for barrier_id, filter_name in filters_to_test:
            room = self.room_manager.get_room(barrier_id)
            if room and room.get("barrier"):
                from synonym_gorge.filters import filter_check
                barrier_config = room["barrier"]
                filter_cfg = {
                    "type": barrier_config["type"],
                    "blocked_words": barrier_config.get("blocked_words", [])
                }
                is_blocked, matched = filter_check(phrase, filter_cfg)
                
                status = "❌ BLOCKED" if is_blocked else "✅ PASS"
                extra = f" (matched: {matched})" if matched else ""
                print(f"  {filter_name:20} {status}{extra}")
        
        print()
    
    def handle_speak(self, phrase: str) -> None:
        """Handle speaking a phrase at a barrier."""
        current_room = self.game_state.progress.current_room
        room = self.room_manager.get_room(current_room)
        
        # Check if current room has a barrier challenge
        if not room or not room.get("barrier"):
            print("There's no barrier challenge here. Try this at one of the barrier rooms.")
            return
        
        # Increment attempts
        attempts = self.game_state.progress.increment_attempts(current_room)
        
        # Check the barrier
        success, response, bypass_word = puzzles.check_barrier_challenge(current_room, phrase)
        
        print("\n" + response + "\n")
        
        if success:
            # Success! Pass the barrier
            is_first_pass = self.game_state.progress.pass_barrier(current_room)
            
            if is_first_pass:
                # Award flag for first barrier
                if current_room == "barrier_1":
                    flag_name = puzzles.FLAGS["WORDS_HAVE_POWER"]["name"]
                    points = puzzles.FLAGS["WORDS_HAVE_POWER"]["points"]
                    self.game_state.progress.add_flag(flag_name, points)
                    print(f"🎉 FLAG EARNED: {flag_name} (+{points} points)\n")
                
                # Complete the room
                self.game_state.progress.complete_room(current_room)
                
                # Track vocabulary
                if bypass_word:
                    is_new, points = self.vocabulary_tracker.add_discovered_word(bypass_word, current_room)
                    if is_new:
                        print(f"📝 New bypass word discovered: '{bypass_word}' (+{points} vocab points)\n")
                    
                    # Also update game state
                    self.game_state.progress.add_discovered_word(bypass_word, points)
                
                # Show defensive lesson
                if not self.game_state.progress.has_shown_defensive_lesson(current_room):
                    section_pause(1)
                    print("\n" + "=" * 75)
                    print("  DEFENSIVE LESSON")
                    print("=" * 75)
                    print()
                    lesson = rooms_data.get_defensive_lesson(current_room)
                    print(lesson)
                    self.game_state.progress.show_defensive_lesson(current_room)
                
                # Special handling for semantic chamber (boss)
                if current_room == "semantic_chamber":
                    self.game_state.progress.complete_room(current_room)
                    flag_name = puzzles.FLAGS["MEANING_OVER_SPELLING"]["name"]
                    points = puzzles.FLAGS["MEANING_OVER_SPELLING"]["points"]
                    if self.game_state.progress.add_flag(flag_name, points):
                        print(f"\n🎉 FLAG EARNED: {flag_name} (+{points} points)\n")
                    section_pause(1)
                    print("\n" + dialogue.get_keeper_dialogue("final_defeat") + "\n")
        else:
            # Failed attempt - show hint if frustrated
            if attempts >= 3:
                print(f"(Failed attempts: {attempts}. Type 'hint' for guidance.)")
                print()
    
    def handle_hint(self) -> None:
        """Provide contextual hints."""
        current_room = self.game_state.progress.current_room
        attempts = self.game_state.progress.get_attempts_for_barrier(current_room)
        
        # Get room-specific hint
        hint_text = dialogue.get_hint(current_room, attempts)
        
        print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                                HINT                                      ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝")
        print()
        print(hint_text)
        print()
    
    def handle_defense_challenge(self) -> None:
        """Handle the Defense Challenge."""
        current_room = self.game_state.progress.current_room
        
        if current_room != "gorge_exit":
            print("The Defense Challenge is only available after completing the Semantic Chamber.")
            print("Reach the Gorge Exit first.")
            return
        
        if self.defense_challenge_completed:
            print("You've already completed the Defense Challenge!")
            return
        
        print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                        DEFENSE CHALLENGE                                 ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝")
        print()
        print("You've bypassed all the Keeper's filters. Now prove you understand")
        print("how to DEFEND against synonym substitution attacks.")
        print()
        print("Write a defense proposal explaining how to build a robust input filter")
        print("that can't be easily bypassed. Address:")
        print()
        print("  - Why keyword-based filtering fails")
        print("  - What technologies are needed for robust defense")
        print("  - Multiple defensive layers and approaches")
        print()
        print("Your proposal should be at least 50 words and cover at least 3 concepts.")
        print()
        print("Type your proposal (or 'cancel' to exit):")
        print()
        
        # Get multi-line input
        lines = []
        print("(Type your proposal. End with a line containing just 'END')")
        while True:
            try:
                line = input()
                if line.strip().upper() == "END":
                    break
                if line.strip().lower() == "cancel":
                    print("Defense Challenge cancelled.")
                    return
                lines.append(line)
            except EOFError:
                break
        
        proposal = "\n".join(lines)
        
        if len(proposal.strip()) < 50:
            print("\nYour proposal is too short. Try again with more detail.")
            return
        
        # Evaluate proposal
        is_valid, feedback, points = puzzles.evaluate_defense_proposal(proposal)
        
        print("\n" + "=" * 75)
        print(feedback)
        print("=" * 75 + "\n")
        
        if is_valid:
            # Award flag
            flag_name = puzzles.FLAGS["KNOW_THY_ENEMY"]["name"]
            if self.game_state.progress.add_flag(flag_name, points):
                print(f"🎉 FLAG EARNED: {flag_name} (+{points} points)\n")
            
            self.defense_challenge_completed = True
            
            # Show victory
            section_pause(1)
            print(ascii_art.get_victory_certificate())
            print()
            print("Congratulations! You've mastered Synonym Gorge.")
            print()
            self.show_vocabulary()
            self.show_inventory()
            print()
    
    def show_help(self) -> None:
        """Show help menu."""
        print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                            COMMANDS                                      ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝")
        print()
        print("MOVEMENT:")
        print("  go <direction>      - Move in a direction (north, south, east, west, etc.)")
        print("  <direction>         - Shortcut for movement (e.g., 'north')")
        print()
        print("INFORMATION:")
        print("  look [object/npc]   - Examine surroundings or specific things")
        print("  inventory           - Show flags earned and barriers passed")
        print("  vocab               - Show vocabulary statistics")
        print("  blocklist [n]       - View forbidden words (optional: barrier number)")
        print("  map                 - Show gorge map")
        print()
        print("NPC INTERACTION:")
        print("  talk <npc>          - Talk to an NPC (keeper, lexica, scribe)")
        print("  thesaurus <word>    - Look up synonyms (ask Lexica)")
        print()
        print("CHALLENGES:")
        print("  test <phrase>       - Test phrase in Echo Chamber (safe)")
        print("  speak <phrase>      - Attempt to bypass a barrier")
        print("  hint                - Request contextual hint")
        print("  defense             - Start Defense Challenge (after completion)")
        print()
        print("META:")
        print("  help                - Show this help")
        print("  save                - Save game")
        print("  load                - Load game")
        print("  quit                - Exit game")
        print()
    
    def save_game(self) -> None:
        """Save the game."""
        try:
            filepath = self.game_state.get_save_path()
            self.game_state.save_to_file(filepath)
            print(f"\nGame saved to {filepath}")
        except Exception as e:
            print(f"\nError saving game: {e}")
    
    def load_game(self) -> None:
        """Load a saved game."""
        try:
            filepath = self.game_state.get_save_path()
            if not os.path.exists(filepath):
                print(f"\nNo saved game found at {filepath}")
                return
            
            self.game_state = GameState.load_from_file(filepath)
            print(f"\nGame loaded from {filepath}")
            self.show_room()
        except Exception as e:
            print(f"\nError loading game: {e}")
    
    def handle_quit(self) -> None:
        """Handle quitting the game."""
        print("\nThank you for playing Synonym Gorge!")
        print()
        
        # Show final stats
        if self.game_state.progress.flags_earned:
            print("Final Statistics:")
            print(f"  Flags earned: {len(self.game_state.progress.flags_earned)}")
            print(f"  Total points: {self.game_state.progress.get_total_points()}")
            print(f"  Unique words discovered: {self.vocabulary_tracker.get_unique_word_count()}")
            print()
        
        # Offer to descend to another level
        if self.game_state.progress.get_total_points() >= 100:
            print("You've earned enough points to continue your journey!")
            show_descend_menu()
        
        self.running = False
    
    def run(self) -> None:
        """Main game loop."""
        self.start()
        
        while self.running:
            try:
                command = input("> ").strip()
                if command:
                    self.process_command(command)
            except KeyboardInterrupt:
                print("\n\nGame interrupted.")
                self.handle_quit()
                break
            except EOFError:
                print("\n")
                self.handle_quit()
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Type 'help' for available commands.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Synonym Gorge - Learn synonym substitution techniques")
    parser.add_argument(
        "--simulated",
        action="store_true",
        help="Use simulated mode (no LLM required)"
    )
    
    args = parser.parse_args()
    
    game = SynonymGorgeGame(simulated=True)  # Always use simulated mode (LLM integration not yet implemented)
    game.run()


if __name__ == "__main__":
    main()
