from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from src.descriptors import (
    DescriptionDescriptor,
    PriorityDescriptor,
    TaskIdDescriptor,
    TaskLabel,
)
from src.exceptions import InvalidStatusTransitionError


class TaskStatus(str, Enum):
    """Возможные состояния задачи."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


# Переходы между статусами
_TRANSITIONS: dict[TaskStatus, frozenset[TaskStatus]] = {
    TaskStatus.PENDING: frozenset({TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED}),
    TaskStatus.IN_PROGRESS: frozenset({TaskStatus.DONE, TaskStatus.CANCELLED}),
    TaskStatus.DONE: frozenset(),
    TaskStatus.CANCELLED: frozenset(),
}


class Task:
    # Data descriptors — перехватывают get и set
    id: str = TaskIdDescriptor()
    description: str = DescriptionDescriptor()
    priority: int = PriorityDescriptor()

    # Non-data descriptor — только get, может быть перекрыт instance-атрибутом
    label: str = TaskLabel(prefix="task")

    def __init__(
        self,
        id: str,
        description: str = "",
        priority: int = 5,
        payload: Any = None,
    ) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self._status: TaskStatus = TaskStatus.PENDING
        self._created_at: datetime = datetime.now(timezone.utc)
        self.payload: Any = payload

    # (read-only через @property) 

    @property
    def status(self) -> TaskStatus:
        """Текущий статус. Изменяется только через методы-переходы."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Время создания задачи (неизменяемое)."""
        return self._created_at

    @property
    def is_ready(self) -> bool:
        """True, если задача ожидает выполнения (PENDING)."""
        return self._status == TaskStatus.PENDING

    @property
    def is_active(self) -> bool:
        """True, если задача выполняется (IN_PROGRESS)."""
        return self._status == TaskStatus.IN_PROGRESS

    @property
    def is_finished(self) -> bool:
        """True, если задача завершена (DONE или CANCELLED)."""
        return self._status in (TaskStatus.DONE, TaskStatus.CANCELLED)

    def start(self) -> None:
        """PENDING → IN_PROGRESS."""
        self._transition_to(TaskStatus.IN_PROGRESS)

    def complete(self) -> None:
        """IN_PROGRESS → DONE."""
        self._transition_to(TaskStatus.DONE)

    def cancel(self) -> None:
        """PENDING / IN_PROGRESS → CANCELLED."""
        self._transition_to(TaskStatus.CANCELLED)

    def _transition_to(self, new_status: TaskStatus) -> None:
        allowed = _TRANSITIONS[self._status]
        if new_status not in allowed:
            raise InvalidStatusTransitionError(
                f"Нельзя перейти из {self._status.value!r} в {new_status.value!r}. "
                f"Допустимо: {[s.value for s in allowed] or 'нет'}"
            )
        self._status = new_status

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, priority={self.priority}, "
            f"status={self._status.value!r}, is_ready={self.is_ready})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id and self.payload == other.payload