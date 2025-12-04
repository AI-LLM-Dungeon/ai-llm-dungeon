#!/usr/bin/env python3
"""
Simple validation script for Ground Level Ollama modules.

This script tests the basic functionality of the educational modules
without requiring Ollama to be installed.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.education.ollama_commands import OllamaOps, CommandResult
from game.education.verification import VerificationHelper
from game.scenes.ground_level import GroundLevelController, ActStatus, VerificationMode


def test_ollama_ops():
    """Test OllamaOps basic functionality."""
    print("Testing OllamaOps...")
    
    # Test is_ollama_available (should work regardless of installation)
    available = OllamaOps.is_ollama_available()
    print(f"  ✓ is_ollama_available() returned: {available}")
    
    # If Ollama is not available, test that commands return appropriate errors
    if not available:
        result = OllamaOps.list_models()
        assert not result.success, "Expected failure when Ollama not available"
        assert result.error_message is not None, "Expected error message"
        print(f"  ✓ Commands properly report when Ollama not available")
    
    print("  OllamaOps tests passed!\n")


def test_verification_helper():
    """Test VerificationHelper functionality."""
    print("Testing VerificationHelper...")
    
    # Test model_exists_in_list
    sample_list = """NAME                ID              SIZE      MODIFIED
llama3:latest       abc123def456    4.7 GB    2 days ago
mistral:latest      def456abc123    4.1 GB    1 day ago"""
    
    assert VerificationHelper.model_exists_in_list('llama3', sample_list), "Should find llama3"
    assert VerificationHelper.model_exists_in_list('mistral', sample_list), "Should find mistral"
    assert not VerificationHelper.model_exists_in_list('qwen', sample_list), "Should not find qwen"
    print("  ✓ model_exists_in_list() works correctly")
    
    # Test model_absent_from_list
    assert VerificationHelper.model_absent_from_list('qwen', sample_list), "qwen should be absent"
    assert not VerificationHelper.model_absent_from_list('llama3', sample_list), "llama3 should not be absent"
    print("  ✓ model_absent_from_list() works correctly")
    
    # Test extract_model_size
    size = VerificationHelper.extract_model_size(sample_list, 'llama3')
    assert size == '4.7 GB', f"Expected '4.7 GB', got '{size}'"
    print("  ✓ extract_model_size() works correctly")
    
    # Test extract_parameter
    sample_show = """Modelfile:
FROM llama3
PARAMETER num_ctx 2048
PARAMETER temperature 0.8"""
    
    num_ctx = VerificationHelper.extract_parameter(sample_show, 'num_ctx')
    assert num_ctx == '2048', f"Expected '2048', got '{num_ctx}'"
    print("  ✓ extract_parameter() works correctly")
    
    # Test contains_keywords
    text = "Artificial intelligence is the simulation of human intelligence"
    assert VerificationHelper.contains_keywords(text, ['AI', 'artificial']), "Should find keywords"
    assert not VerificationHelper.contains_keywords(text, ['robot', 'machine']), "Should not find absent keywords"
    print("  ✓ contains_keywords() works correctly")
    
    # Test is_valid_list_output
    assert VerificationHelper.is_valid_list_output(sample_list), "Should validate list output"
    assert not VerificationHelper.is_valid_list_output("random text"), "Should reject invalid output"
    print("  ✓ is_valid_list_output() works correctly")
    
    # Test is_valid_show_output
    assert VerificationHelper.is_valid_show_output(sample_show), "Should validate show output"
    assert not VerificationHelper.is_valid_show_output("random text"), "Should reject invalid output"
    print("  ✓ is_valid_show_output() works correctly")
    
    # Test response_received
    assert VerificationHelper.response_received("AI is artificial intelligence"), "Should accept valid response"
    assert not VerificationHelper.response_received(""), "Should reject empty response"
    assert not VerificationHelper.response_received("Error: failed"), "Should reject error messages"
    print("  ✓ response_received() works correctly")
    
    print("  VerificationHelper tests passed!\n")


def test_ground_level_controller():
    """Test GroundLevelController functionality."""
    print("Testing GroundLevelController...")
    
    # Test initialization with different modes
    controller_shell = GroundLevelController(verification_mode="shell")
    assert controller_shell.verification_mode == VerificationMode.SHELL
    print("  ✓ Shell mode initialization works")
    
    controller_paste = GroundLevelController(verification_mode="paste")
    assert controller_paste.verification_mode == VerificationMode.PASTE
    print("  ✓ Paste mode initialization works")
    
    controller_sim = GroundLevelController(verification_mode="simulated")
    assert controller_sim.verification_mode == VerificationMode.SIMULATED
    print("  ✓ Simulated mode initialization works")
    
    # Test start_act
    payload = controller_shell.start_act(1)
    assert payload.act_number == 1
    assert payload.title == "Summoner's Vestibule"
    assert controller_shell.act_statuses[1] == ActStatus.IN_PROGRESS
    print("  ✓ start_act() works correctly")
    
    # Test get_act_status
    status = controller_shell.get_act_status()
    assert status['current_act'] == 1
    assert status['total_acts'] == 5
    assert status['completed_count'] == 0
    print("  ✓ get_act_status() works correctly")
    
    # Test simulated verification (always succeeds)
    result = controller_sim.verify_act(1)
    assert result.success
    assert controller_sim.act_statuses[1] == ActStatus.COMPLETED
    print("  ✓ Simulated verification works")
    
    # Test paste verification with valid input
    controller_paste2 = GroundLevelController(verification_mode="paste")
    sample_list = "llama3:latest    abc123    4.7 GB    2 days ago"
    result = controller_paste2.verify_act(1, sample_list)
    assert result.success
    print("  ✓ Paste verification works")
    
    # Test loading quest JSON
    quest_path = os.path.join(os.path.dirname(__file__), '../content/quests/ground_level.json')
    if os.path.exists(quest_path):
        controller_json = GroundLevelController(quest_json_path=quest_path)
        assert controller_json.quest_data is not None
        print("  ✓ Quest JSON loading works")
    
    print("  GroundLevelController tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Ground Level Ollama Module Validation")
    print("=" * 60 + "\n")
    
    try:
        test_ollama_ops()
        test_verification_helper()
        test_ground_level_controller()
        
        print("=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
