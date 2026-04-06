# Лабораторная работа №2: Модель задачи — дескрипторы и `@property`
 
**Цель**: Освоить управление доступом к атрибутам и защиту инвариантов доменной модели.
 
**Описание**: В этом проекте реализована полноценная модель задачи `Task` с валидацией через пользовательские дескрипторы, защищёнными и вычисляемыми свойствами через `@property`, управлением жизненным циклом задачи и специализированными исключениями.
 
## 1) Установка проекта локально
```bash
git clone https://github.com/TheVailen/python_lab2_descriptors.git
cd python_lab2_descriptors
python3.11 -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov
```
 
## 2) Что добавлено и изменено
 
| Категория | Функции/Классы |
| :--- | :--- |
| **Исключения** | `TaskError`, `InvalidTaskIdError`, `InvalidDescriptionError`, `InvalidPriorityError`, `InvalidStatusTransitionError` |
| **Data дескрипторы** | `TaskIdDescriptor`, `DescriptionDescriptor`, `PriorityDescriptor` |
| **Non-data дескриптор** | `TaskLabel` — демонстрация перекрытия instance-атрибутом |
| **Модель задачи** | `Task` — атрибуты с валидацией, `@property`, переходы статусов |
| **Статусы** | `TaskStatus`: `PENDING` → `IN_PROGRESS` → `DONE` / `CANCELLED` |
| **Вычисляемые свойства** | `is_ready`, `is_active`, `is_finished` |
| **Защищённые свойства** | `status`, `created_at` — только для чтения |
| **Тестирование** | `test_models.py` — тесты дескрипторов, переходов, `@property` |
 
### Ключевые архитектурные решения
 
**Data vs Non-data дескриптор:**
- Data (`TaskIdDescriptor`, `PriorityDescriptor`, `DescriptionDescriptor`) — реализуют `__get__` + `__set__`, перехватывают запись и выполняют валидацию
- Non-data (`TaskLabel`) — реализует только `__get__`. Instance-атрибут с тем же именем перекрывает его, так как `instance.__dict__` имеет приоритет
 
**`@property` для защиты инвариантов:**
- `status` и `created_at` — только для чтения, изменяются только через методы класса
- `is_ready`, `is_active`, `is_finished` — вычисляемые, производные от `status`
 
## 3) Запуск программы
 
```bash
python -m src.main
```
 
### Вывод
```
=== Источники задач ===
file-1: {"action": "process_order", "order_id": 101}
file-2: {"action": "send_notification", "user_id": 7}
gen-1: {"action": "recalculate_stats"}
gen-2: {"action": "check_resource"}
api-1: {"action": "sync_external_data"}
api-2: {"action": "rebuild_cache"}
 
=== Модель Task: дескрипторы и @property ===
Создана: Task(id='demo-1', priority=7, status='pending', is_ready=True)
is_ready=True, is_active=False, is_finished=False
label (non-data descriptor): task:demo-1
После start(): status=in_progress, is_active=True
После complete(): status=done, is_finished=True
 
Non-data descriptor до перекрытия: task:demo-2
Non-data descriptor после перекрытия: custom-label
 
=== Исключения при нарушении инвариантов ===
InvalidTaskIdError: id должен быть непустой строкой, получено ''
InvalidPriorityError: Приоритет должен быть от 1 до 10, получено 99
InvalidStatusTransitionError: Нельзя перейти из 'pending' в 'done'
```
 
## 4) Тесты
 
```bash
python -m pytest -v
```
 
### Тесты с процентом покрытия
```bash
python -m pytest --cov=src
```
 
## 5) Запуск в Docker
 
```bash
docker build -t python-lab2 .
docker run --rm python-lab2
docker run --rm python-lab2 python -m pytest tests -v
```
 
## 6) Библиотеки и модули
 
| Категория | Модуль | Назначение |
| :--- | :--- | :--- |
| **Типизация** | `typing` | `Protocol`, `runtime_checkable`, аннотации типов |
| **Модели данных** | `dataclasses` | Источники задач через `@dataclass` |
| **Перечисления** | `enum` | `TaskStatus` через `str, Enum` |
| **Дата и время** | `datetime` | Время создания задачи |
| **Коллекции** | `collections.abc` | `Iterable`, `Callable` |
| **Файлы** | `pathlib` | Работа с путями к JSONL-файлам |
| **JSON** | `json` | Чтение задач из JSONL-файла |
| **Тестирование** | `pytest` | Проверка корректности модулей |
| **Покрытие** | `pytest-cov` | Подсчёт процента покрытия |
| **Контейнеризация** | `Docker` | Переносимый запуск проекта |
 
## 7) Чему я научился
 
* Реализовал data и non-data дескрипторы и разобрался в их различиях: data-дескриптор имеет приоритет над `instance.__dict__`, а non-data - нет
* Научился использовать `@property` для защиты инвариантов и создания вычисляемых свойств
* Реализовал управление жизненным циклом объекта через явные переходы между состояниями с проверкой допустимости
* Освоил создание иерархии специализированных исключений для доменных ошибок
* Научился разделять публичный API и внутреннее состояние объекта