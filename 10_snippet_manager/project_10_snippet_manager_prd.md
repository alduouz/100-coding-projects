
# Project 10: Snippet Manager CLI App - PRD

## 1. Overview
Develop a command-line application to manage reusable code snippets. Users can add, list, search, and export snippets in JSON storage. The application will use `argparse` to support subcommands for different operations and will persist data between runs.

## 2. Functional Requirements
### 2.1 Commands
- **add**:
  - Prompt for snippet description (required).
  - Prompt for snippet code (required).
  - Prompt for optional tags (comma-separated).
  - Store with a unique ID, created_at timestamp, and tags as a lowercase list.
- **list**:
  - Display all snippets with their ID, description, tags, and created_at date.
- **search**:
  - Search by keyword across description, code, and tags (case-insensitive).
  - Display matching snippets.
- **export**:
  - Export all snippets to either `.md` (Markdown) or `.txt` (plain text).
  - Markdown export: fenced code blocks.
  - Text export: plain text with headings.

### 2.2 Storage
- File format: JSON array of snippet objects.
- Fields: `id`, `description`, `code`, `tags`, `created_at`.
- Persist data in `snippets.json` (configurable via CLI argument).

### 2.3 CLI Behavior
- Use `argparse` with subcommands (`add`, `list`, `search`, `export`).
- For `add`, if no arguments are passed, prompt interactively.
- Output should be human-readable and clearly formatted.

### 2.4 Validation
- Description and code are mandatory; print an error if missing.
- Tags optional, but if provided, normalize to lowercase.

## 3. Non-functional Requirements
- Python 3.8+.
- Standard library only (`argparse`, `json`, `os`, `uuid`, `datetime`).
- Code organized into small, testable functions.
- Ensure no data loss on save (atomic write).

## 4. Testing Requirements
### 4.1 Unit Tests
- **Storage**:
  - Adding a snippet writes correct data to JSON.
  - Search returns correct results for keyword in description, code, or tags.
  - Export produces correct file format and content.
- **CLI**:
  - Simulate `add` with CLI arguments (non-interactive) and verify persistence.
  - Simulate `list` and capture output to verify correct formatting.
  - Simulate `search` with known keyword and verify matching results in output.
  - Simulate `export` and check exported file content for correctness.
- Use `tempfile.TemporaryDirectory()` to isolate test data.
- Inject `print_func` or capture `stdout` for CLI output verification.

## 5. User Stories
- **As a developer**, I want to store and search for code snippets so I can reuse them easily.
- **As a developer**, I want to export my snippets for sharing or backup.

## 6. Acceptance Criteria
- Running `python snippet_manager.py add` prompts for description, code, and tags and saves to JSON.
- Running `python snippet_manager.py list` displays all stored snippets.
- Running `python snippet_manager.py search <keyword>` displays only matching snippets.
- Running `python snippet_manager.py export --format md` produces a Markdown file with all snippets in fenced code blocks.
- All unit tests pass with `python -m unittest`.

## 7. Deliverables
- `snippet_manager.py` main CLI file.
- `snippets.json` data file (runtime).
- `test_snippet_manager.py` with all required tests.

## 8. Lessons Learned
- Designing CLI tools with subcommands.
- Managing persistent data in JSON.
- Structuring applications for easy unit testing.
