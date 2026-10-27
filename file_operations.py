"""Пакетная проверка и текстовые отчёты."""

from pathlib import Path

from history import make_record
from validator import validate_email


def check_file(path):
    # utf-8-sig также поддерживает UTF-8 с BOM.
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    if not lines:
        raise ValueError("Входной файл пуст")
    return [make_record(line, *validate_email(line)) for line in lines]


def format_record(record):
    message = f"{record['email']} — {record['result']}"
    if record["reason"]:
        message += f": {record['reason']}"
    return message


def save_report(path, records):
    Path(path).write_text(
        "\n".join(format_record(row) for row in records) + "\n",
        encoding="utf-8",
    )
