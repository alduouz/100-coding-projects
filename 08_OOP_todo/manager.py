from typing import List, Optional, Literal
import json
import os
import tempfile
from datetime import datetime
from models import Task


def atomic_save(obj, path: str) -> None:
    """Atomically save object to JSON file with UTF-8 encoding.
    
    Args:
        obj: Object to serialize to JSON
        path: Target file path
    """
    dir_ = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile("w", dir=dir_, delete=False, encoding="utf-8") as tmp:
        json.dump(obj, tmp, indent=2, ensure_ascii=False)
        tmp_name = tmp.name
    os.replace(tmp_name, path)


class TaskManager:
    """Manages a collection of tasks with persistent JSON storage."""
    
    def __init__(self, storage_path: str = "tasks.json"):
        """Initialize TaskManager with specified storage path.
        
        Args:
            storage_path: Path to JSON file for task storage
        """
        self.tasks: List[Task] = []
        self.storage_path: str = storage_path
    
    def load(self) -> None:
        """Load tasks from JSON file with schema defaults and error handling."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.tasks = []
                        for item in data:
                            try:
                                task = Task.from_dict(item)
                                self.tasks.append(task)
                            except (ValueError, TypeError) as e:
                                # Skip invalid tasks but continue loading others
                                continue
            else:
                self.tasks = []
        except (json.JSONDecodeError, FileNotFoundError, PermissionError):
            # If file is corrupted or inaccessible, start with empty list
            self.tasks = []
    
    def save(self) -> None:
        """Save tasks to JSON file using atomic write with UTF-8 encoding."""
        try:
            task_dicts = [task.to_dict() for task in self.tasks]
            atomic_save(task_dicts, self.storage_path)
        except (OSError, PermissionError) as e:
            # In a production app, we might want to notify the user
            # For now, silently fail but preserve in-memory tasks
            pass
    
    def add(self, description: str, due_date: Optional[str] = None) -> Task:
        """Add a new task and save immediately.
        
        Args:
            description: Task description (non-empty)
            due_date: Optional due date in YYYY-MM-DD format
            
        Returns:
            The created Task instance
            
        Raises:
            ValueError: If description is empty
        """
        if due_date == "":
            due_date = None
        
        task = Task(description=description, due_date=due_date)
        self.tasks.append(task)
        self.save()
        return task
    
    def delete_by_index(self, index: int) -> Task:
        """Delete task by 1-based index from current view.
        
        Args:
            index: 1-based index of task to delete
            
        Returns:
            The deleted Task instance
            
        Raises:
            IndexError: If index is out of range
        """
        if index < 1 or index > len(self.tasks):
            raise IndexError(f"Task index {index} is out of range")
        
        deleted_task = self.tasks.pop(index - 1)
        self.save()
        return deleted_task
    
    def complete_by_index(self, index: int) -> Task:
        """Mark task complete by 1-based index from current view.
        
        Args:
            index: 1-based index of task to complete
            
        Returns:
            The completed Task instance
            
        Raises:
            IndexError: If index is out of range
        """
        if index < 1 or index > len(self.tasks):
            raise IndexError(f"Task index {index} is out of range")
        
        task = self.tasks[index - 1]
        task.mark_complete()
        self.save()
        return task
    
    def list_all(self) -> List[Task]:
        """Return all tasks.
        
        Returns:
            List of all Task instances
        """
        return self.tasks.copy()
    
    def filter_completed(self, flag: bool) -> List[Task]:
        """Return tasks filtered by completion status.
        
        Args:
            flag: True for completed tasks, False for incomplete tasks
            
        Returns:
            List of filtered Task instances
        """
        return [task for task in self.tasks if task.completed == flag]
    
    def sorted_by(self, field: Literal["created_at", "due_date"]) -> List[Task]:
        """Return tasks sorted by specified field.
        
        Args:
            field: Field to sort by ("created_at" or "due_date")
            
        Returns:
            List of sorted Task instances
        """
        if field == "created_at":
            return sorted(self.tasks, key=lambda t: t.created_at)
        elif field == "due_date":
            # Sort by due_date, putting None values at the end
            return sorted(self.tasks, key=lambda t: (t.due_date is None, t.due_date or ""))
        else:
            return self.tasks.copy()