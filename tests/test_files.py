"""Проверки файлов и сохранения истории."""

import json
import tempfile
import unittest
from pathlib import Path

from file_operations import check_file, save_report
from history import append_history, load_history


class FileTests(unittest.TestCase):
    def test_batch_report_and_persistent_history(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "emails.txt"
            source.write_text("user@example.com\n@domain.com\n\n",
                              encoding="utf-8-sig")
            records = check_file(source)
            self.assertEqual(len(records), 3)
            self.assertEqual(records[0]["result"], "корректен")
            self.assertEqual(records[2]["reason"], "Пустой адрес")
            save_report(root / "report.txt", records)
            self.assertIn("Нет локальной части",
                          (root / "report.txt").read_text(encoding="utf-8"))
            history = root / "history.json"
            append_history(history, records)
            append_history(history, records[:1])
            self.assertEqual(len(load_history(history)), 4)

    def test_file_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.txt"
            with self.assertRaises(FileNotFoundError):
                check_file(path)
            path.touch()
            with self.assertRaises(ValueError):
                check_file(path)
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeError):
                check_file(path)

    def test_corrupt_history_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "history.json"
            for content in ("broken", '{}', '[{}]'):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises((ValueError, json.JSONDecodeError)):
                    append_history(path, [])
                self.assertEqual(path.read_text(encoding="utf-8"), content)
