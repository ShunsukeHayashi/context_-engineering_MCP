from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import uuid

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class AgentType(Enum):
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"
    SPECIALIST = "specialist"

class WorkflowStatus(Enum):
    CREATED = "created"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Agent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: AgentType = AgentType.SPECIALIST
    capabilities: List[str] = field(default_factory=list)
    max_concurrent_tasks: int = 3
    current_tasks: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def is_available(self) -> bool:
        return len(self.current_tasks) < self.max_concurrent_tasks
    
    @property
    def load_percentage(self) -> float:
        return (len(self.current_tasks) / self.max_concurrent_tasks) * 100

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: Optional[int] = None  # minutes
    actual_duration: Optional[int] = None
    priority: int = 5  # 1-10, 10 being highest
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    errors: List[str] = field(default_factory=list)
    
    @property
    def is_ready(self) -> bool:
        """Check if all dependencies are completed"""
        return self.status == TaskStatus.PENDING and len(self.dependencies) == 0
    
    @property
    def duration_minutes(self) -> Optional[int]:
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds() / 60)
        return None

@dataclass
class Workflow:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.CREATED
    tasks: List[Task] = field(default_factory=list)
    agents: List[Agent] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def progress_percentage(self) -> float:
        if not self.tasks:
            return 0.0
        completed_tasks = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        return (completed_tasks / len(self.tasks)) * 100
    
    @property
    def task_distribution(self) -> Dict[TaskStatus, int]:
        distribution = {status: 0 for status in TaskStatus}
        for task in self.tasks:
            distribution[task.status] += 1
        return distribution
    
    def get_ready_tasks(self) -> List[Task]:
        """Get tasks that are ready to be executed"""
        completed_task_ids = {task.id for task in self.tasks if task.status == TaskStatus.COMPLETED}
        ready_tasks = []
        
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                if all(dep_id in completed_task_ids for dep_id in task.dependencies):
                    ready_tasks.append(task)
        
        return sorted(ready_tasks, key=lambda t: t.priority, reverse=True)
    
    def get_available_agents(self) -> List[Agent]:
        """Get agents that can take on new tasks"""
        return [agent for agent in self.agents if agent.is_available]