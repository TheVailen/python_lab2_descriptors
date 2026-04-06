from __future__ import annotations

import json
from pathlib import Path

from src.intake import TaskIntake
from src.sources import ApiStubSource, GeneratorSource, JsonlFileSource
from src.contracts import Task

from src.exceptions import InvalidPriorityError, InvalidStatusTransitionError


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

    intake = TaskIntake([
        JsonlFileSource(demo_file),
        GeneratorSource(demo_generator),
        ApiStubSource([
            {"id": "api-1", "payload": {"action": "sync_external_data"}},
            {"payload": {"action": "rebuild_cache"}},
        ]),
    ])

    print("=== Источники задач ===")
    for task in intake.iter_tasks():
        print(f"{task.id}: {json.dumps(task.payload, ensure_ascii=False)}")

    # Демонстрация модели Task (Лаба 2) 
    print("\n=== Модель Task: дескрипторы и @property ===")

    task = Task(id="demo-1", description="Обработать заказ", priority=7)
    print(f"Создана: {task!r}")
    print(f"is_ready={task.is_ready}, is_active={task.is_active}, is_finished={task.is_finished}")
    print(f"label (non-data descriptor): {task.label}")

    task.start()
    print(f"После start(): status={task.status.value}, is_active={task.is_active}")

    task.complete()
    print(f"После complete(): status={task.status.value}, is_finished={task.is_finished}")

    # Non-data descriptor: instance-атрибут перекрывает дескриптор
    task2 = Task(id="demo-2", description="Тест", priority=3)
    print(f"\nNon-data descriptor до перекрытия: {task2.label}")
    task2.label = "custom-label" 
    print(f"Non-data descriptor после перекрытия: {task2.label}")

    print("\n=== Исключения при нарушении инвариантов ===")
    try:
        Task(id="", description="bad id")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

    try:
        Task(id="x", priority=99)
    except InvalidPriorityError as e:
        print(f"{type(e).__name__}: {e}")

    try:
        t = Task(id="t-1")
        t.complete()
    except InvalidStatusTransitionError as e:
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()