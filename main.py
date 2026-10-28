"""Консольный валидатор email. Запуск: python3 main.py."""

import json
from pathlib import Path

from file_operations import check_file, format_record, save_report
from history import append_history, load_history, make_record
from validator import validate_email

HISTORY_PATH = Path(__file__).resolve().parent / "history.json"


def ask_path(prompt):
    value = input(prompt).strip()
    if not value:
        raise ValueError("Путь к файлу не может быть пустым")
    return Path(value).expanduser().resolve()


def run_action(choice):
    if choice == "1":
        address = input("Введите email: ")
        record = make_record(address, *validate_email(address))
        print(format_record(record))
        append_history(HISTORY_PATH, [record])
        print("Проверка сохранена в истории.")
    elif choice == "2":
        source = ask_path("Путь к списку адресов: ")
        target = ask_path("Путь к новому файлу отчёта: ")
        if source == target or target == HISTORY_PATH:
            raise ValueError("Для отчёта нужен отдельный файл")
        if target.exists():
            raise ValueError("Файл отчёта уже существует: выберите новое имя")
        records = check_file(source)
        # Проверяем историю до записи отчёта, чтобы выявить повреждение.
        load_history(HISTORY_PATH)
        save_report(target, records)
        print(f"Отчёт сохранён: {target}. Проверено адресов: {len(records)}")
        append_history(HISTORY_PATH, records)
        print("Проверки сохранены в истории.")
    elif choice == "3":
        records = load_history(HISTORY_PATH)
        if not records:
            print("История пока пуста.")
        for record in records[-20:]:
            print(f"{record['time']} | {format_record(record)}")
    else:
        print("Неизвестный пункт. Введите 0, 1, 2 или 3.")


def main():
    while True:
        print("\n1. Проверить email\n2. Проверить файл"
              "\n3. Последние 20 проверок\n0. Выход")
        try:
            choice = input("Выберите действие: ").strip()
            if choice == "0":
                print("До свидания!")
                return
            run_action(choice)
        except UnicodeError:
            print("Ошибка кодировки: используйте файл в UTF-8.")
        except json.JSONDecodeError:
            print("История повреждена. Сохраните её копию и исправьте JSON "
                  "или переместите файл history.json перед новой проверкой.")
        except (OSError, ValueError) as error:
            print(f"Операция не завершена: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nПрограмма завершена.")
            return


if __name__ == "__main__":
    main()
