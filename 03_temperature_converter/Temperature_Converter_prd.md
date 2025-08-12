# PRD – Project 3: Temperature Converter

## 1. **Title & Summary**
**Title:** CLI Temperature Converter  
**Summary:**  
A Python command-line application that converts between Celsius and Fahrenheit.  
Users choose the direction of conversion, input a temperature, and receive the converted value.  
The program repeats until the user chooses to exit.

---

## 2. **Objectives**
- Reinforce function-based programming in Python.
- Practice clean CLI user flows with validation.
- Introduce looped workflows for repeated user interactions.
- Implement robust error handling for bad inputs.

---

## 3. **Scope**
**In-Scope:**
- Celsius → Fahrenheit conversion.
- Fahrenheit → Celsius conversion.
- Continuous execution until user exits.
- Input validation for numeric values.
- Graceful handling of invalid selections.

**Out-of-Scope:**
- GUI or web interface.
- Kelvin or other temperature scales.
- File storage or persistence.

---

## 4. **Functional Requirements**
1. **Conversion Options**  
   - Prompt: “Select conversion type: 1) Celsius to Fahrenheit  2) Fahrenheit to Celsius”
   - Accept numeric choice (1 or 2).  
   - Any other input prompts retry.

2. **Temperature Input**  
   - Prompt user for a temperature value.  
   - Must be a valid float (e.g., `37.5`, `-10`).  
   - Invalid values trigger an error message and re-prompt.

3. **Conversion Logic**  
   - Celsius → Fahrenheit: `F = C * 9/5 + 32`  
   - Fahrenheit → Celsius: `C = (F - 32) * 5/9`  
   - Each conversion implemented as a **separate function**.

4. **Looped Flow**  
   - After each conversion, ask “Do you want to convert another? (y/n)”  
   - If yes, restart flow; if no, exit with a goodbye message.

---

## 5. **Non-Functional Requirements**
- Written in Python 3.x
- Fewer than 100 lines of code.
- Inline comments explaining key steps.
- Functions must be named descriptively (e.g., `celsius_to_fahrenheit`, not `c2f`).
- No external libraries beyond standard Python.

---

## 6. **Technical Stack**
- **Language:** Python 3.x
- **Runtime:** Local terminal execution
- **No third-party dependencies**

---

## 7. **User Flow**
```
[Start Program]
      ↓
Display menu: 1) C → F  |  2) F → C
      ↓
User selects option
      ↓
Prompt: "Enter temperature:"
      ↓
Validate input (retry if invalid)
      ↓
Perform conversion
      ↓
Display result
      ↓
"Do you want to convert another? (y/n)"
      ↓
Yes → Repeat from start
No → Exit with message
```

---

## 8. **Acceptance Criteria**
- **Case 1:** User selects C → F, inputs `0` → Output is `32.0°F`
- **Case 2:** User selects F → C, inputs `212` → Output is `100.0°C`
- **Case 3:** User enters invalid temperature → Error message + retry prompt
- **Case 4:** User enters invalid menu choice → Error message + retry prompt
- **Case 5:** Program loops until user enters `n` or `no` at “convert another?” prompt

---

## 9. **Edge Cases**
- Large numbers (e.g., `9999`) should still work without crashing.
- Negative temperatures must be accepted (e.g., `-40`).
- User input with leading/trailing spaces (e.g., `" 100 "`).
- Non-numeric values for temperature should be caught and handled.
- Case-insensitive `y/n` input (`Y`, `Yes`, `n`, `No`).
