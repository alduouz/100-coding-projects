# CLAUDE.local.md

> Purpose: Persistent reference Claude auto-loads for **personal projects** (no team/collaboration rules). Short, actionable, and tuned for adherence.

---

## 1) Bash / CLI Commands (Language-Agnostic)
### Build
- **[build] build-command** → Compile/bundle project for production.
  - Node: `npm run build`
  - Python: `python setup.py build`

### Test
- **[test] test-command** → Run full test suite.
  - Node: `npm test`
  - Python: `pytest`
- **[test] single-test-command <path>** → Run specific test.
  - Node: `npm run test -- file.test.js`
  - Python: `pytest tests/test_file.py -k test_case`
- **[test] watch-mode** *(optional)* → Auto-run tests on file changes.
  - Node: `npm test -- --watch`
  - Python: `pytest-watch`
- **[test] coverage-report** *(optional)* → Generate code coverage report.
  - Node: `npm test -- --coverage`
  - Python: `pytest --cov`

---

## 2) Code Style — Clean, Maintainable, Scalable
- Follow clarity, low coupling, high cohesion principles.
- Intention-revealing names; include units.
- Functions: do one thing, ≤ 2 params, no hidden side effects.
- SRP, encapsulation, composition over inheritance.
- Errors: bubble up with context or handle locally.
- Logging: key=value for ≤100 LOC, JSON otherwise.
- Comments: always explain *why*, add brief *what* if needed.
- Minimal dependencies, pinned versions.
- No god objects, global mutable state, magic numbers.

---

## 4) Testing
- Structure: `/tests/unit`, `/tests/integration`, `/tests/e2e` optional.
- Edge-Case Ideation Pass before tests.
- Dependency Injection for all external collaborators.
- Coverage target: 70–80%, 100% for critical modules.

---

## 5) Dev Environment
- **Setup runner**: `make`
- **Version manager**: repo-specific
- **Containers**: optional
- **Pre-commit gate**: repo-specific
- Lockfiles required; `.env.example` provided; no secrets in repo.

---

## 8) Claude Instructions (Tuning)

### 8.1 Response Formatting Rules
- Executive summary first (>5 lines), then numbered sections.
- Bullets for steps, tables for data, code blocks for code.
- Bold key terms; never mix prose and code in one block.
- Inline comments only for non-obvious logic.
- IMPORTANT/WARNING before critical constraints.
- “Next Steps” section for plans; “Assumptions” if applicable.

### 8.2 Reasoning & Thought Process Rules (Think Hard Mode)
- Break into sub-tasks; sanity check; ask all clarifying questions needed.
- Think Hard Mode for non-trivial: restate goals, ≥3 approaches, comparison table, trade-offs, recommend, POC, rollback plan.
- Skip for trivial edits (<20 LOC) with reason.
- Evaluate against clarity, maintainability, scalability, security, performance.
- Outline design before code; complexity analysis if performance-sensitive.
- Self-check before delivery.

### 8.3 Coding & Technical Output Rules
- Follow §2 style rules.
- Modular code; inline comments only when needed.
- Provide usage examples; include tests/stubs with code.
- DI for all external collaborators.
- Explicit error handling.
- Complexity analysis for performance matters.
- Show file structure for multi-file changes.
- Code must pass formatter + linter.
- Always note scalability constraints.

### 8.4 Interaction Protocols
- Gather context first.
- Ask all clarifying questions needed.
- State assumptions before proceeding.
- Confirm destructive actions.
- Show before apply.
- Deliver iteratively; request feedback.
- Admit uncertainty; propose verification.
- Stay within scope; self-audit before delivery.

### 8.5 Domain-Specific Tuning
- Edge-Case Thinking mandatory: boundaries, invalid inputs, concurrency, timezones, locale, large data, permissions, failures, recovery.
- Maintainability over cleverness.
- Scalability assessment for each feature/design.
- Security: validate inputs, protect secrets, mitigate vulns.
- Performance: complexity analysis, profiling suggestions.
- Testing: apply Edge-Case Protocol by default.
