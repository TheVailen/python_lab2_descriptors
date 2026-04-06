from __future__ import annotations


class TaskError(Exception):
    """Базовое исключение для доменных ошибок Task."""


class InvalidTaskIdError(TaskError):
    """Недопустимый идентификатор задачи."""


class InvalidDescriptionError(TaskError):
    """Недопустимое описание задачи."""


class InvalidPriorityError(TaskError):
    """Приоритет выходит за допустимый диапазон."""


class InvalidStatusTransitionError(TaskError):
    """Недопустимый переход между статусами."""