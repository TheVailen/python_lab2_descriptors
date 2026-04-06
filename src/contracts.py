from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from src.models import Task
from src.models import TaskStatus as TaskStatus

@runtime_checkable
class TaskSource(Protocol):
    """Единый контракт для всех источников задач."""

    name: str

    def get_tasks(self) -> Iterable[Task]:
        """Вернуть задачи из источника."""