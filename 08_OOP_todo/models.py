from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class Task:
    """Represents a single task with UUID identifier, description, completion status, and optional due date."""
    
    def __init__(self, description: str, due_date: Optional[str] = None, id: Optional[str] = None, 
                 completed: bool = False, created_at: Optional[str] = None):
        """Initialize a new Task.
        
        Args:
            description: Non-empty task description
            due_date: Optional due date in YYYY-MM-DD format
            id: Optional UUID string (generates new if not provided)
            completed: Task completion status (default: False)
            created_at: Optional creation timestamp (uses current time if not provided)
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        self.id: str = id or str(uuid.uuid4())
        self.description: str = description.strip()
        self.completed: bool = completed
        self.due_date: Optional[str] = due_date
        self.created_at: str = created_at or datetime.now().isoformat()
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        """Create Task instance from dictionary with schema defaults and validation.
        
        Args:
            data: Dictionary containing task data
            
        Returns:
            Task instance with validated and defaulted fields
        """
        description = data.get("description", "")
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        # Set defaults for missing fields
        completed = data.get("completed", False)
        due_date = data.get("due_date")
        if due_date == "":
            due_date = None
        created_at = data.get("created_at")
        if not created_at:
            created_at = datetime.now().isoformat()
        
        return Task(
            description=description,
            due_date=due_date,
            id=data.get("id"),
            completed=completed,
            created_at=created_at
        )
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "✗"
        due_info = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.description}{due_info}"