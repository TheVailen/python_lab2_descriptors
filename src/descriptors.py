from __future__ import annotations

from typing import Any

from src.exceptions import (
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidTaskIdError,
)

class TaskIdDescriptor:
    """Data descriptor: id — непустая строка"""

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> str:
        if obj is None:
            return self 
        return getattr(obj, self._attr)

    def __set__(self, obj: Any, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidTaskIdError(
                f"id должен быть непустой строкой, получено {value!r}"
            )
        object.__setattr__(obj, self._attr, value.strip())


class DescriptionDescriptor:
    """Data descriptor: описание — строка до 500 символов"""

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> str:
        if obj is None:
            return self  
        return getattr(obj, self._attr, "")

    def __set__(self, obj: Any, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidDescriptionError(
                f"Описание должно быть строкой, получено {value!r}"
            )
        if len(value) > 500:
            raise InvalidDescriptionError(
                "Описание не должно превышать 500 символов"
            )
        object.__setattr__(obj, self._attr, value)


class PriorityDescriptor:
    """Data descriptor: c приоритетом целое число от 1 до 10"""

    MIN: int = 1
    MAX: int = 10

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> int:
        if obj is None:
            return self  
        return getattr(obj, self._attr, 5)

    def __set__(self, obj: Any, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidPriorityError(
                f"Приоритет должен быть int, получено {value!r}"
            )
        if not (self.MIN <= value <= self.MAX):
            raise InvalidPriorityError(
                f"Приоритет должен быть от {self.MIN} до {self.MAX}, получено {value}"
            )
        object.__setattr__(obj, self._attr, value)


class TaskLabel:
    """Non-data descriptor: вычисляет метку задачи на основе id"""


    def __init__(self, prefix: str = "task") -> None:
        self._prefix = prefix

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> str:
        if obj is None:
            return f"{self._prefix}:<class>"
        task_id = getattr(obj, "_id", "unknown")
        return f"{self._prefix}:{task_id}"