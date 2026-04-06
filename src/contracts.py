from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class Task:
    """Представление задачи."""

    id: str
    payload: Any


@runtime_checkable
class TaskSource(Protocol):
    """Единый контракт для всех источников задач."""

    name: str

    def get_tasks(self) -> Iterable[Task]:
        """Вернуть задачи из источника."""