
# Project 8: To‑Do List (OOP Refactor) — PRD

## 1) Overview
Refactor the Project 7 procedural to‑do CLI into an **object‑oriented** design. Introduce `Task` and `TaskManager` classes, stable UUID identifiers, and dependency injection for I/O (so the app is fully testable). Preserve JSON persistence with **atomic writes** and explicit UTF‑8 encodings.

## 2) Objectives
- Practice **object modeling** (entities, responsibilities, invariants).
- Improve **testability** (inject input/print and storage path).
- Upgrade **data integrity** (atomic save).
- Prepare for future features (filters, sorting, editing) via clear class interfaces.

## 3) Functional Requirements
### 3.1 Entities
- **Task**
  - Fields: `id: str` (UUID4), `description: str` (non‑empty), `completed: bool` (default False), `due_date: Optional[str]` (YYYY‑MM‑DD), `created_at: str` (ISO 8601).
  - Methods:
    - `mark_complete() -> None`
    - `to_dict() -> Dict[str, Any]` / `@staticmethod from_dict(d: Dict[str, Any]) -> "Task"` (performs schema defaults & validation).

- **TaskManager**
  - Fields: `tasks: List[Task]`, `storage_path: str`
  - Methods:
    - `load() -> None` — loads tasks from JSON (with schema defaults).
    - `save() -> None` — atomic write to JSON using UTF‑8.
    - `add(description: str, due_date: Optional[str]) -> Task`
    - `delete_by_index(index: int) -> Task` (1‑based index from current view)
    - `complete_by_index(index: int) -> Task`
    - `list_all() -> List[Task]`
    - (Optional) `filter_completed(flag: bool) -> List[Task]`
    - (Optional) `sorted_by(field: Literal["created_at","due_date"]) -> List[Task]`

### 3.2 CLI
- Menu (loop until exit): **Add**, **List**, **Complete**, **Delete**, **Exit**.
- Numbered output for list view; display `[✓/✗]`, description, and `(Due: YYYY‑MM‑DD)` when set.
- Inputs:
  - Description (required, non‑empty).
  - Due date (optional). If provided, must parse with `%Y-%m-%d`; re‑prompt until valid or empty.
- After every mutation (**add/complete/delete**), **save immediately**.

### 3.3 Persistence
- File name default: `tasks.json` (configurable).
- JSON schema: array of task objects.
- **Atomic write** and **UTF‑8** encodings. Ensure ASCII not forced (allow non‑ASCII descriptions).

## 4) Non‑Functional Requirements
- Python 3.8+.
- Standard library only (`json`, `uuid`, `dataclasses` optional, `tempfile`, `os`, `datetime`, `typing`).
- **Dependency injection** for I/O:
  - `input_func: Callable[[str], str] = input`
  - `print_func: Callable[[str], None] = print`
- Modules must include **type hints** and docstrings.
- Handle errors gracefully; never crash on malformed JSON or invalid input.
- Keep cyclomatic complexity per method low; prefer small, focused methods.

## 5) Acceptance Criteria
- Starting with an empty/nonexistent `tasks.json`, the app can **add**, **list**, **complete**, **delete** tasks successfully.
- Invalid menu choice or task number shows a clear message and re‑prompts.
- Entering an invalid date re‑prompts (or Enter to skip).
- After app restart, previously added tasks are present (persistence verified).
- `tasks.json` writes are **atomic**; no partial/corrupt files after simulated interruptions.
- IDs remain **stable** across operations (no reindexing IDs).

## 6) Implementation Notes
- Use `uuid.uuid4()` for `Task.id`.
- `created_at`: `datetime.now().isoformat()`.
- In `Task.from_dict`, set defaults:
  - `completed=False` if missing
  - `due_date=None` if missing/empty
  - `created_at=now` if missing
- Normalize due date to `YYYY‑MM‑DD` when provided; store `None` otherwise.
- Atomic save pattern:
  ```python
  import tempfile, os, json
  def atomic_save(obj: Any, path: str) -> None:
      dir_ = os.path.dirname(path) or "."
      with tempfile.NamedTemporaryFile("w", dir=dir_, delete=False, encoding="utf-8") as tmp:
          json.dump(obj, tmp, indent=2, ensure_ascii=False)
          tmp_name = tmp.name
      os.replace(tmp_name, path)
  ```

## 7) Suggested File Layout
```
todo_oop/
  ├─ todo.py              # CLI entrypoint (constructs TaskManager, injects I/O)
  ├─ models.py            # Task dataclass / class
  ├─ manager.py           # TaskManager class
  ├─ storage.json         # (runtime) tasks.json
  └─ tests/               # (optional) unit tests
```

## 8) Stretch Goals (Optional)
- Filters: list only completed / only pending.
- Sorting: by due date or created_at.
- Edit task description / due date.
- Export to Markdown or CSV.
- Colorized CLI (e.g., `colorama`) — keep optional and behind a flag.

## 9) Example CLI Flow
```
--- To‑Do List (OOP) ---
1. Add Task
2. List Tasks
3. Mark Task Complete
4. Delete Task
5. Exit
Enter choice: 1
Description: Buy milk
Due date (YYYY‑MM‑DD, Enter to skip): 2025-08-20
Task 'Buy milk' added!

Enter choice: 2

--- Your Tasks ---
1. [✗] Buy milk (Due: 2025-08-20)
```

## 10) Deliverables
- Source files as described above (single‑file also acceptable if well‑structured).
- `tasks.json` created at runtime.
- Screenshot of a sample run demonstrating all features.
- (Optional) tests showing add/list/complete/delete happy paths and invalid inputs.
