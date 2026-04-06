from __future__ import annotations

from pathlib import Path

import pytest

from src.contracts import Task
from src.sources import ApiStubSource, GeneratorSource, JsonlFileSource


def test_file_source_reads_tasks(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.jsonl"
    file_path.write_text(
        '{"id": "task-1", "payload": {"action": "process_order"}}\n'
        '{"id": "task-2", "payload": [1, 2, 3]}\n',
        encoding="utf-8",
    )

    source = JsonlFileSource(file_path)

    assert list(source.get_tasks()) == [
        Task(id="task-1", payload={"action": "process_order"}),
        Task(id="task-2", payload=[1, 2, 3]),
    ]


def test_file_source_rejects_invalid_json(tmp_path: Path) -> None:
    file_path = tmp_path / "bad.jsonl"
    file_path.write_text('{"id": "task-1", "payload": }\n', encoding="utf-8")

    source = JsonlFileSource(file_path)

    with pytest.raises(ValueError, match="Invalid JSON"):
        list(source.get_tasks())


def test_file_source_rejects_missing_fields(tmp_path: Path) -> None:
    file_path = tmp_path / "bad.jsonl"
    file_path.write_text('{"id": "task-1"}\n', encoding="utf-8")

    source = JsonlFileSource(file_path)

    with pytest.raises(ValueError, match="must contain id and payload"):
        list(source.get_tasks())


def test_generator_source_returns_generated_tasks() -> None:
    def producer():
        yield Task(id="g-1", payload={"action": "notify"})
        yield Task(id="g-2", payload={"action": "recalculate"})

    source = GeneratorSource(producer)

    assert list(source.get_tasks()) == [
        Task(id="g-1", payload={"action": "notify"}),
        Task(id="g-2", payload={"action": "recalculate"}),
    ]


def test_api_source_returns_tasks() -> None:
    source = ApiStubSource(
        [
            {"id": "api-1", "payload": {"action": "check_resource"}},
            {"payload": {"action": "send_email"}},
        ]
    )

    assert list(source.get_tasks()) == [
        Task(id="api-1", payload={"action": "check_resource"}),
        Task(id="api-2", payload={"action": "send_email"}),
    ]


def test_api_source_rejects_missing_payload() -> None:
    source = ApiStubSource([{"id": "bad"}])

    with pytest.raises(ValueError, match="must contain payload"):
        list(source.get_tasks())

def test_file_source_rejects_non_object_json(tmp_path: Path) -> None:
    file_path = tmp_path / "bad.jsonl"
    file_path.write_text('[1, 2, 3]\n', encoding="utf-8")

    source = JsonlFileSource(file_path)

    with pytest.raises(ValueError, match="must be a JSON object"):
        list(source.get_tasks())
