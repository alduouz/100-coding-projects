# PRD – Project 4: Number Guessing Game (Python CLI)

## 1. Title & Summary
**Title:** Number Guessing Game (1–100)  
**Summary:**  
A Python command-line game where the computer picks a random integer between 1 and 100.  
The user guesses until correct, receiving **Too high** / **Too low** feedback each attempt.  
Tracks total guesses and supports replaying the game without restarting the program.

---

## 2. Objectives
- Practice loops, branching, and state (attempt counter).
- Introduce Python's `random` module.
- Reinforce robust input validation and user flow design.
- Prepare for future games/apps that maintain state across steps.

---

## 3. Scope
**In-Scope:**
- Random number generation within a fixed range (default 1–100).
- Validated numeric guesses with feedback per attempt.
- Attempt counting and end-of-round summary.
- Option to replay without exiting the program.

**Out-of-Scope:**
- GUI/web interface.
- Difficulty levels or leaderboards (can be added as stretch).

---

## 4. Functional Requirements
1. **Start a Round**
   - Generate a secret integer in **[1, 100]** using `random.randint(1, 100)`.
   - Show a brief greeting and rules (e.g., “Guess a number between 1 and 100”).

2. **User Guess Loop**
   - Prompt for a guess until correct.
   - Validate input is an integer; on invalid input, show an error and re-prompt **without** counting the attempt.
   - If guess < secret → print **"Too low!"**; if guess > secret → **"Too high!"**.

3. **Win & Summary**
   - When correct, print **"Correct!"** and the number of valid attempts.
   - Offer to **play again (y/n)**; on `y` start a new round with a fresh secret.

4. **State & Counters**
   - Maintain an **attempt counter** (counts only valid numeric guesses).
   - Reset the counter each new round.

---

## 5. Non-Functional Requirements
- Python 3.x; standard library only.
- Clear, consistent prompts and messages.
- Fewer than ~120 LOC (not strict; clarity first).
- Functions with descriptive names (e.g., `play_round()`, `get_valid_guess()`).
- Inline comments for key logic (random, loop, counters).

---

## 6. Technical Stack
- **Language:** Python 3.x
- **Libraries:** `random` from the stdlib
- **Runtime:** Local terminal

---

## 7. User Flow
```
[Program start]
  ↓
Print welcome + rules
  ↓
Start round → pick secret in [1,100]
  ↓
Loop:
  - Prompt "Enter your guess:"
  - If invalid → show error → re-prompt (do not increment attempts)
  - If valid:
      - attempts += 1
      - Compare to secret:
          < → "Too low!"
          > → "Too high!"
          = → "Correct!" → print attempts → ask "Play again? (y/n)"
              - y → new round (new secret, reset attempts)
              - n → exit with goodbye
```

---

## 8. Acceptance Criteria
- **AC1:** Secret is always an integer in **[1,100]**.
- **AC2:** Invalid inputs (e.g., `"abc"`, `""`, `"3.14"`) do **not** increment attempts and re-prompt.
- **AC3:** Valid integer guesses produce correct directional feedback.
- **AC4:** On correct guess, program prints `"Correct!"` and attempts count.
- **AC5:** `y/yes` (case-insensitive) restarts; `n/no` exits gracefully.

---

## 9. Edge Cases
- Leading/trailing spaces in input (e.g., `"  50 "`).
- Negative numbers or zero (out of range) → treat as valid integers but give directional feedback (**"Too low!"**).
- Very large integers → directional feedback (**"Too high!"**), no crash.
- Repeated guesses allowed; still count as attempts.
- Case-insensitive replay inputs: `Y`, `Yes`, `n`, `NO`, etc.

---

## 10. Suggested Function Decomposition
- `def get_valid_guess() -> int:`  ⟶ loops until the user provides a valid **integer**.
- `def play_round() -> int:`       ⟶ generates secret, loops guesses, returns attempts on win.
- `def ask_play_again() -> bool:`   ⟶ returns True for yes, False for no.
- `def main():`                     ⟶ game loop controlling multiple rounds.

---

## 11. Example Transcript
```
Welcome to Number Guessing!
I'm thinking of a number between 1 and 100.
Enter your guess: 60
Too high!
Enter your guess: 30
Too low!
Enter your guess: 45
Correct! You got it in 3 attempts.
Play again? (y/n): y

I'm thinking of a number between 1 and 100.
Enter your guess: abc
Invalid input. Please enter an integer.
Enter your guess: 50
Too high!
Enter your guess: 25
Correct! You got it in 2 attempts.
Play again? (y/n): n
Thanks for playing. Goodbye!
```

---

## 12. Incremental Learning vs Project 3
| Project | Key Concept Added |
|--------|--------------------|
| 3 – Temperature Converter | Deterministic math, menu branching, input validation, looped flow |
| 4 – Number Guessing Game  | **Randomness & stateful loops**, attempt counters, replayable rounds, tighter UX around invalid inputs |

---

## 13. Optional Stretch Features (Nice-to-Haves)
- **Attempt limit** (e.g., max 7 guesses) → lose state & reveal secret.
- **Hints** after N attempts (e.g., “The number is divisible by 3”).
- **Difficulty levels** (1–50, 1–100, 1–1000).
- **Stats** across rounds (best score, average attempts).
- **Seeded RNG** for deterministic testing (e.g., `random.seed(42)`).

---

## 14. Claude Prompt (for code generation)
> "Write a Python 3 CLI number guessing game. The computer picks a random integer in [1,100]. I repeatedly enter guesses until correct. Use functions (`play_round`, `get_valid_guess`, `ask_play_again`). Count only **valid integer** guesses. Invalid input re-prompts without incrementing attempts. Print 'Too high!' / 'Too low!' hints. On correct guess, print attempts and ask to play again (y/n). Use only the standard library."
