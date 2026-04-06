from __future__ import annotations

import json
from pathlib import Path

from src.intake import TaskIntake
from src.sources import ApiStubSource, GeneratorSource, JsonlFileSource
from src.contracts import Task


def demo_generator():
    yield Task(id="gen-1", payload={"action": "recalculate_stats"})
    yield Task(id="gen-2", payload={"action": "check_resource"})


def main() -> None:
    demo_file = Path("demo_tasks.jsonl")
    demo_file.write_text(
        '{"id": "file-1", "payload": {"action": "process_order", "order_id": 101}}\n'
        '{"id": "file-2", "payload": {"action": "send_notification", "user_id": 7}}\n',
        encoding="utf-8",
    )

    file_source = JsonlFileSource(demo_file)
    generator_source = GeneratorSource(demo_generator)
    api_source = ApiStubSource(
        [
            {"id": "api-1", "payload": {"action": "sync_external_data"}},
            {"payload": {"action": "rebuild_cache"}},
        ]
    )

    intake = TaskIntake([file_source, generator_source, api_source])

    for task in intake.iter_tasks():
        print(f"{task.id}: {json.dumps(task.payload, ensure_ascii=False)}")


if __name__ == "__main__":
    main()