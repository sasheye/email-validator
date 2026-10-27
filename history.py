"""Хранение истории проверок в JSON."""

import json
from datetime import datetime
from pathlib import Path


def load_history(path):
    """Загрузить историю, проверив структуру записей."""
    path = Path(path)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or any(
        not isinstance(row, dict)
        or not all(isinstance(row.get(key), str)
                   for key in ("time", "email", "result", "reason"))
        or row["result"] not in ("корректен", "некорректен")
        for row in data
    ):
        raise ValueError("Неверная структура истории")
    return data


def make_record(address, valid, reason):
    return {
        "time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "email": address,
        "result": "корректен" if valid else "некорректен",
        "reason": reason,
    }


def append_history(path, records):
    """Сохранить историю через временный файл рядом с целевым."""
    path = Path(path)
    data = load_history(path) + records
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
