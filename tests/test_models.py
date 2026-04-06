from __future__ import annotations

import pytest

from src.exceptions import (
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidStatusTransitionError,
    InvalidTaskIdError,
)
from src.models import Task, TaskStatus

def test_task_created_with_defaults() -> None:
    task = Task(id="t-1")
    assert task.id == "t-1"
    assert task.description == ""
    assert task.priority == 5
    assert task.status == TaskStatus.PENDING
    assert task.payload is None


def test_task_created_with_all_fields() -> None:
    task = Task(id="t-2", description="Описание", priority=8, payload={"x": 1})
    assert task.id == "t-2"
    assert task.description == "Описание"
    assert task.priority == 8
    assert task.payload == {"x": 1}

def test_created_at_is_immutable() -> None:
    task = Task(id="t-3")
    with pytest.raises(AttributeError):
        task.created_at = None 

def test_id_strips_whitespace() -> None:
    task = Task(id="  t-1  ")
    assert task.id == "t-1"

def test_id_empty_raises() -> None:
    with pytest.raises(InvalidTaskIdError):
        Task(id="")

def test_id_whitespace_only_raises() -> None:
    with pytest.raises(InvalidTaskIdError):
        Task(id="   ")

def test_id_non_string_raises() -> None:
    with pytest.raises(InvalidTaskIdError):
        Task(id=123) 

def test_description_too_long_raises() -> None:
    with pytest.raises(InvalidDescriptionError):
        Task(id="t-1", description="x" * 501)

def test_description_non_string_raises() -> None:
    with pytest.raises(InvalidDescriptionError):
        Task(id="t-1", description=42) 

def test_priority_out_of_range_raises() -> None:
    with pytest.raises(InvalidPriorityError):
        Task(id="t-1", priority=11)

    with pytest.raises(InvalidPriorityError):
        Task(id="t-1", priority=0)


def test_priority_bool_raises() -> None:
    with pytest.raises(InvalidPriorityError):
        Task(id="t-1", priority=True)


def test_priority_boundary_values() -> None:
    assert Task(id="a", priority=1).priority == 1
    assert Task(id="b", priority=10).priority == 10

def test_is_ready_pending() -> None:
    task = Task(id="t-1")
    assert task.is_ready is True
    assert task.is_active is False
    assert task.is_finished is False

def test_is_active_after_start() -> None:
    task = Task(id="t-1")
    task.start()
    assert task.is_ready is False
    assert task.is_active is True
    assert task.is_finished is False

def test_is_finished_after_complete() -> None:
    task = Task(id="t-1")
    task.start()
    task.complete()
    assert task.is_finished is True

def test_is_finished_after_cancel() -> None:
    task = Task(id="t-1")
    task.cancel()
    assert task.is_finished is True

def test_status_cannot_be_set_directly() -> None:
    task = Task(id="t-1")
    with pytest.raises(AttributeError):
        task.status = TaskStatus.DONE  

def test_full_lifecycle() -> None:
    task = Task(id="t-1")
    assert task.status == TaskStatus.PENDING
    task.start()
    assert task.status == TaskStatus.IN_PROGRESS
    task.complete()
    assert task.status == TaskStatus.DONE

def test_cannot_complete_from_pending() -> None:
    task = Task(id="t-1")
    with pytest.raises(InvalidStatusTransitionError):
        task.complete()

def test_cannot_start_finished_task() -> None:
    task = Task(id="t-1")
    task.start()
    task.complete()
    with pytest.raises(InvalidStatusTransitionError):
        task.start()

def test_cannot_transition_from_done() -> None:
    task = Task(id="t-1")
    task.start()
    task.complete()
    with pytest.raises(InvalidStatusTransitionError):
        task.cancel()

def test_label_computed_from_id() -> None:
    task = Task(id="abc-1")
    assert task.label == "task:abc-1"

def test_label_can_be_shadowed_by_instance_attribute() -> None:
    """Non-data descriptor не имеет __set__, поэтому instance-атрибут его перекрывает"""
    task = Task(id="abc-1")
    task.label = "custom" 
    assert task.label == "custom"