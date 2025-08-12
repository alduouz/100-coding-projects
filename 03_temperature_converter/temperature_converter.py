#!/usr/bin/env python3

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit using the formula F = C * 9/5 + 32"""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius using the formula C = (F - 32) * 5/9"""
    return (fahrenheit - 32) * 5/9

def get_conversion_choice():
    """Get user's choice for conversion type with validation"""
    while True:
        print("\nSelect conversion type:")
        print("1) Celsius to Fahrenheit")
        print("2) Fahrenheit to Celsius")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            return 1
        elif choice == "2":
            return 2
        else:
            print("Invalid choice. Please enter 1 or 2.")

def get_temperature_input():
    """Get temperature value from user with validation"""
    while True:
        temp_input = input("Enter temperature: ").strip()
        
        try:
            temperature = float(temp_input)
            return temperature
        except ValueError:
            print("Invalid temperature. Please enter a numeric value.")

def ask_continue():
    """Ask user if they want to perform another conversion"""
    while True:
        response = input("Do you want to convert another? (y/n): ").strip().lower()
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    """Main program loop for temperature converter"""
    print("Welcome to the Temperature Converter!")
    
    while True:
        # Get conversion choice
        choice = get_conversion_choice()
        
        # Get temperature input
        temperature = get_temperature_input()
        
        # Perform conversion and display result
        if choice == 1:
            # Celsius to Fahrenheit
            result = celsius_to_fahrenheit(temperature)
            print(f"{temperature}°C = {result:.1f}°F")
        else:
            # Fahrenheit to Celsius
            result = fahrenheit_to_celsius(temperature)
            print(f"{temperature}°F = {result:.1f}°C")
        
        # Ask if user wants to continue
        if not ask_continue():
            print("Thank you for using the Temperature Converter! Goodbye!")
            break

if __name__ == "__main__":
    main()