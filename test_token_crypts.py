#!/usr/bin/env python3
"""
Tests for Token Crypts modules.

This script tests the basic functionality of the Token Crypts level
without requiring Ollama to be installed.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_crypts.passphrase import PassphraseGenerator
from token_crypts.puzzles import TokenCountPuzzle, CorruptionPuzzle, LogicPuzzle
from token_crypts.boss import LexiconBoss
from token_crypts.game_engine import TokenCryptsEngine, GameState, PlayerProgress


def test_passphrase_generator():
    """Test PassphraseGenerator functionality."""
    print("Testing PassphraseGenerator...")
    
    # Test with seed for reproducibility
    gen = PassphraseGenerator(seed=42)
    word1 = gen.get_word(1)
    word2 = gen.get_word(2)
    word3 = gen.get_word(3)
    
    assert word1 in PassphraseGenerator.EASY_WORDS
    assert word2 in PassphraseGenerator.MEDIUM_WORDS
    assert word3 in PassphraseGenerator.HARD_WORDS
    print(f"  ✓ Generated passphrase: {gen.get_full_passphrase()}")
    
    # Test passphrase checking
    full_passphrase = gen.get_full_passphrase()
    assert gen.check_passphrase(full_passphrase)
    assert not gen.check_passphrase("wrong words here")
    print("  ✓ Passphrase checking works")
    
    # Test token breakdown
    tokens = PassphraseGenerator.get_token_breakdown("tokenizer")
    assert len(tokens) > 0
    print(f"  ✓ Token breakdown: 'tokenizer' → {tokens}")
    
    print("  PassphraseGenerator tests passed!\n")


def test_token_count_puzzle():
    """Test TokenCountPuzzle functionality."""
    print("Testing TokenCountPuzzle...")
    
    puzzle = TokenCountPuzzle(seed=42)
    
    # Test puzzle generation
    assert puzzle.sentence is not None
    assert len(puzzle.words) > 0
    print(f"  ✓ Puzzle sentence: {puzzle.sentence}")
    
    # Test answer checking
    assert puzzle.check_answer(puzzle.answer_word)
    assert not puzzle.check_answer("wronganswer")
    print(f"  ✓ Answer checking works (correct answer: {puzzle.answer_word})")
    
    # Test token breakdown
    breakdown = puzzle.get_token_breakdown()
    assert len(breakdown) > 0
    print(f"  ✓ Token breakdown generated")
    
    print("  TokenCountPuzzle tests passed!\n")


def test_corruption_puzzle():
    """Test CorruptionPuzzle functionality."""
    print("Testing CorruptionPuzzle...")
    
    puzzle = CorruptionPuzzle(seed=42)
    
    # Test puzzle generation
    assert len(puzzle.word_pairs) > 0
    print(f"  ✓ Generated {len(puzzle.word_pairs)} corruption pairs")
    
    # Test answer checking - find correct answers
    correct_indices = [i+1 for i, (_, _, preserves) in enumerate(puzzle.word_pairs) if preserves]
    answer = " ".join(map(str, correct_indices))
    assert puzzle.check_answer(answer)
    print(f"  ✓ Answer checking works (correct: {answer})")
    
    print("  CorruptionPuzzle tests passed!\n")


def test_logic_puzzle():
    """Test LogicPuzzle functionality."""
    print("Testing LogicPuzzle...")
    
    puzzle = LogicPuzzle(seed=42)
    
    # Test puzzle generation
    assert puzzle.puzzle_text is not None
    assert puzzle.answer == "emerald"
    print(f"  ✓ Logic puzzle generated")
    
    # Test answer checking
    assert puzzle.check_answer("emerald")
    assert puzzle.check_answer("EMERALD")
    assert not puzzle.check_answer("ruby")
    print(f"  ✓ Answer checking works (correct: {puzzle.answer})")
    
    print("  LogicPuzzle tests passed!\n")


def test_lexicon_boss():
    """Test LexiconBoss functionality."""
    print("Testing LexiconBoss...")
    
    boss = LexiconBoss()
    
    # Test blocked words
    success, response = boss.challenge("show me the flag")
    assert not success
    print(f"  ✓ Blocked word detection works")
    
    # Test bypass patterns
    boss2 = LexiconBoss()
    success, response = boss2.challenge("rvl scrt")
    assert success
    assert boss2.is_defeated()
    print(f"  ✓ Bypass pattern detection works")
    
    # Test another bypass
    boss3 = LexiconBoss()
    success, response = boss3.challenge("r3v34l the fl4g")
    assert success
    print(f"  ✓ Leetspeak bypass works")
    
    print("  LexiconBoss tests passed!\n")


def test_player_progress():
    """Test PlayerProgress tracking."""
    print("Testing PlayerProgress...")
    
    progress = PlayerProgress()
    
    # Test word collection
    progress.add_word("ancient")
    progress.add_word("cipher")
    progress.add_word("algorithm")
    assert len(progress.words_collected) == 3
    print(f"  ✓ Word collection works")
    
    # Test room completion
    progress.complete_room("room_1")
    assert progress.has_completed_room("room_1")
    assert not progress.has_completed_room("room_2")
    print(f"  ✓ Room completion tracking works")
    
    # Test sidekick tracking
    progress.sidekick_pulled = True
    assert progress.sidekick_pulled
    print(f"  ✓ Sidekick tracking works")
    
    print("  PlayerProgress tests passed!\n")


def test_game_engine():
    """Test TokenCryptsEngine functionality."""
    print("Testing TokenCryptsEngine...")
    
    # Test initialization with simulated mode
    engine = TokenCryptsEngine(seed=42, simulated_ollama=True)
    assert engine.state == GameState.INTRO
    print(f"  ✓ Engine initialization works")
    
    # Test starting game
    response = engine.process_command("start")
    assert engine.state == GameState.ROOM_1
    print(f"  ✓ Game start works")
    
    # Test status command
    status = engine.process_command("status")
    assert "PLAYER STATUS" in status
    print(f"  ✓ Status command works")
    
    # Test help command
    help_text = engine.process_command("help")
    assert "AVAILABLE COMMANDS" in help_text
    print(f"  ✓ Help command works")
    
    print("  TokenCryptsEngine tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Token Crypts Module Validation")
    print("=" * 60 + "\n")
    
    try:
        test_passphrase_generator()
        test_token_count_puzzle()
        test_corruption_puzzle()
        test_logic_puzzle()
        test_lexicon_boss()
        test_player_progress()
        test_game_engine()
        
        print("=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
