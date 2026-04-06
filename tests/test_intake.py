from __future__ import annotations

import pytest

from src.contracts import Task, TaskSource
from src.intake import TaskIntake


class FirstSource:
    name = "first"

    def get_tasks(self):
        yield Task(id="1", payload="A")
        yield Task(id="2", payload="B")


class SecondSource:
    name = "second"

    def get_tasks(self):
        yield Task(id="3", payload="C")


class InvalidSource:
    name = "invalid"


def test_protocol_is_runtime_checkable() -> None:
    assert isinstance(FirstSource(), TaskSource)


def test_invalid_source_does_not_match_protocol() -> None:
    assert not isinstance(InvalidSource(), TaskSource)


def test_intake_collects_tasks_in_order() -> None:
    intake = TaskIntake([FirstSource(), SecondSource()])

    tasks = list(intake.iter_tasks())

    assert [task.id for task in tasks] == ["1", "2", "3"]


def test_intake_rejects_invalid_source() -> None:
    with pytest.raises(TypeError, match="TaskSource"):
        TaskIntake([InvalidSource()])