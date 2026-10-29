"""Проверки правил учебного валидатора."""

import unittest
import sys
from pathlib import Path

# При прямом запуске добавляем корень проекта для импорта модулей.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validator import validate_email


class ValidatorTests(unittest.TestCase):
    def test_valid_addresses(self):
        for address in ("user@example.com", "first.last@sub.domain.co.uk",
                        "name+tag@example.org", "a_b-c@my-domain.ru"):
            with self.subTest(address=address):
                self.assertEqual(validate_email(address), (True, ""))

    def test_invalid_addresses_have_reason(self):
        for address in ("", "@domain.com", "user@.com.ua", "user@domain",
                        "user@domain..com", "a@@example.com", "a b@ex.com",
                        ".a@ex.com", "a..b@ex.com", "a@-ex.com",
                        "a@ex-.com", "a@ex.c", "a@ex.toolong",
                        "a@ex.12", "я@ex.ru", "a!@ex.com", "a@"):
            with self.subTest(address=address):
                valid, reason = validate_email(address)
                self.assertFalse(valid)
                self.assertTrue(reason)


if __name__ == "__main__":
    unittest.main()
