#!/usr/bin/env python3

from calculator import calculate

def test_calculator():
    # Test basic operations
    assert calculate(5, 3, '+') == 8
    assert calculate(5, 3, '-') == 2
    assert calculate(5, 3, '*') == 15
    assert calculate(6, 3, '/') == 2
    
    # Test with decimals
    assert calculate(5.5, 2.5, '+') == 8.0
    assert calculate(10.0, 4.0, '/') == 2.5
    
    # Test division by zero
    try:
        calculate(5, 0, '/')
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_calculator()