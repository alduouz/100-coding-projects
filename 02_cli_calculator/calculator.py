#!/usr/bin/env python3
import operator

OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

VALID_OPERATORS = frozenset(OPERATORS.keys())

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_operator():
    while True:
        op = input("Enter an operator (+, -, *, /): ").strip()
        if op in VALID_OPERATORS:
            return op
        print("Invalid operator. Please enter one of: +, -, *, /")

def calculate(num1, num2, op):
    if op == '/' and num2 == 0:
        raise ValueError("Cannot divide by zero")
    return OPERATORS[op](num1, num2)

def get_continue_choice():
    valid_yes = frozenset(['y', 'yes'])
    valid_no = frozenset(['n', 'no'])
    
    while True:
        choice = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if choice in valid_yes:
            return True
        elif choice in valid_no:
            return False
        print("Please enter 'y' for yes or 'n' for no.")

def main():
    print("Welcome to the CLI Calculator!")
    
    while True:
        try:
            num1 = get_number("Enter the first number: ")
            num2 = get_number("Enter the second number: ")
            op = get_operator()
            
            result = calculate(num1, num2, op)
            print(f"\nResult: {num1} {op} {num2} = {result}")
            
            if not get_continue_choice():
                print("Thank you for using the calculator!")
                break
            print()
                    
        except ValueError as e:
            print(f"Error: {e}")
            print("Let's try again.\n")

if __name__ == "__main__":
    main()