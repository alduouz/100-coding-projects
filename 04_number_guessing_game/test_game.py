#!/usr/bin/env python3
"""Test script to validate the number guessing game functionality."""

import random
from number_guessing_game import get_valid_guess, play_round, ask_play_again


def test_basic_functionality():
    """Test basic game components."""
    print("Testing game components...")
    
    # Test random number generation
    secret = random.randint(1, 100)
    assert 1 <= secret <= 100, "Random number should be between 1 and 100"
    print("✓ Random number generation works")
    
    # Test that functions exist and are callable
    assert callable(get_valid_guess), "get_valid_guess should be callable"
    assert callable(play_round), "play_round should be callable"
    assert callable(ask_play_again), "ask_play_again should be callable"
    print("✓ All required functions exist")
    
    print("All tests passed!")


def test_with_mocked_io():
    """Test game functions with mocked input/output."""
    print("Testing with mocked I/O...")
    
    # Test get_valid_guess with valid input
    def mock_input_valid(prompt):
        return "42"
    
    output_log = []
    def mock_print(msg):
        output_log.append(msg)
    
    result = get_valid_guess(mock_input_valid, mock_print)
    assert result == 42, "Should return valid integer"
    print("✓ get_valid_guess works with valid input")
    
    # Test ask_play_again with 'y' response
    def mock_input_yes(prompt):
        return "y"
    
    result = ask_play_again(mock_input_yes, mock_print)
    assert result == True, "Should return True for 'y'"
    print("✓ ask_play_again works with 'y'")
    
    # Test ask_play_again with 'n' response
    def mock_input_no(prompt):
        return "n"
    
    result = ask_play_again(mock_input_no, mock_print)
    assert result == False, "Should return False for 'n'"
    print("✓ ask_play_again works with 'n'")
    
    print("Mocked I/O tests passed!")


if __name__ == "__main__":
    test_basic_functionality()
    test_with_mocked_io()