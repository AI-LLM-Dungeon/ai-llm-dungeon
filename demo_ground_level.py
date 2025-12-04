#!/usr/bin/env python3
"""
Demo script showing how to use the Ground Level Ollama modules.

This demonstrates the three verification modes and basic usage patterns.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.scenes.ground_level import GroundLevelController


def demo_simulated_mode():
    """Demonstrate simulated mode (no Ollama required)."""
    print("\n" + "=" * 60)
    print("DEMO: Simulated Mode")
    print("=" * 60)
    print("In simulated mode, commands are shown but not executed.")
    print("Progress is tracked without verification.\n")
    
    controller = GroundLevelController(verification_mode="simulated")
    
    # Start Act 1
    print("Starting Act 1...")
    payload = controller.start_act(1)
    print(f"Title: {payload.title}")
    print(f"Objective: {payload.objective}")
    print(f"Command: {payload.command_hint}\n")
    
    # Verify Act 1 (auto-completes in simulated mode)
    result = controller.verify_act(1)
    print(f"Verification: {result.message}")
    print(f"Next: {result.next_step}\n")
    
    # Show status
    status = controller.get_act_status()
    print(f"Progress: {status['completed_count']}/{status['total_acts']} acts completed")


def demo_paste_mode():
    """Demonstrate paste mode."""
    print("\n" + "=" * 60)
    print("DEMO: Paste Mode")
    print("=" * 60)
    print("In paste mode, you execute commands in your terminal")
    print("and paste the output for verification.\n")
    
    controller = GroundLevelController(verification_mode="paste")
    
    # Start Act 1
    print("Starting Act 1...")
    payload = controller.start_act(1)
    print(f"Title: {payload.title}")
    print(f"Command to run: {payload.command_hint}")
    print("\nAfter running 'ollama list', paste output like:")
    print("llama3:latest    abc123    4.7 GB    2 days ago\n")
    
    # Simulate pasted output
    sample_paste = "llama3:latest    abc123def456    4.7 GB    2 days ago"
    result = controller.verify_act(1, sample_paste)
    print(f"Verification: {result.message}")
    print(f"Next: {result.next_step}")


def demo_shell_mode():
    """Demonstrate shell mode (requires Ollama)."""
    print("\n" + "=" * 60)
    print("DEMO: Shell Mode")
    print("=" * 60)
    print("In shell mode, commands are executed automatically.")
    print("This requires Ollama to be installed.\n")
    
    controller = GroundLevelController(verification_mode="shell")
    
    # Check if Ollama is available
    from game.education.ollama_commands import OllamaOps
    if not OllamaOps.is_ollama_available():
        print("⚠️  Ollama is not installed or not in PATH.")
        print("Shell mode requires Ollama. Skipping this demo.")
        print("Visit https://ollama.ai to install Ollama.\n")
        return
    
    # Start Act 1
    print("Starting Act 1...")
    payload = controller.start_act(1)
    print(f"Title: {payload.title}")
    print(f"Command: {payload.command_hint}")
    print("\nExecuting verification...")
    
    # Verify (will execute 'ollama list')
    result = controller.verify_act(1)
    print(f"Verification: {result.message}")
    if result.shell_output:
        print(f"Shell output:\n{result.shell_output[:200]}...")


def demo_full_quest():
    """Demonstrate a complete quest run in simulated mode."""
    print("\n" + "=" * 60)
    print("DEMO: Full Quest (Simulated)")
    print("=" * 60)
    print("Completing all 5 acts in simulated mode...\n")
    
    quest_path = os.path.join(
        os.path.dirname(__file__),
        'content/quests/ground_level.json'
    )
    
    controller = GroundLevelController(
        verification_mode="simulated",
        quest_json_path=quest_path if os.path.exists(quest_path) else None
    )
    
    for act_num in range(1, 6):
        print(f"Act {act_num}:", end=" ")
        payload = controller.start_act(act_num)
        result = controller.verify_act(act_num)
        print(f"{payload.title} - {result.message}")
    
    print()
    status = controller.get_act_status()
    print(f"Quest Complete! {status['completed_count']}/{status['total_acts']} acts completed")
    print("\nCommands Mastered:")
    print("  • ollama pull - Download models")
    print("  • ollama list - List installed models")
    print("  • ollama run - Execute models with prompts")
    print("  • ollama show - Inspect model details")
    print("  • ollama rm - Remove models")


def main():
    """Run all demos."""
    print("=" * 60)
    print("Ground Level Ollama Module Demo")
    print("=" * 60)
    print("\nThis script demonstrates the three verification modes")
    print("and basic usage of the Ground Level modules.\n")
    
    try:
        demo_simulated_mode()
        demo_paste_mode()
        demo_shell_mode()
        demo_full_quest()
        
        print("\n" + "=" * 60)
        print("Demo complete!")
        print("=" * 60)
        print("\nTo integrate these modules into your game UI:")
        print("1. Import GroundLevelController")
        print("2. Choose verification mode (shell/paste/simulated)")
        print("3. Call start_act() to get act information")
        print("4. Display teaching text and command hints to user")
        print("5. Call verify_act() to check completion")
        print("6. Display verification results and next steps")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
