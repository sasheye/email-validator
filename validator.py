"""Проверка email по правилам учебного задания."""

import re

# Локальная часть состоит из непустых групп, разделённых точками.
# Части домена не начинаются и не заканчиваются дефисом.
# Последняя часть домена содержит 2–6 латинских букв.
EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9_+\-]+(?:\.[A-Za-z0-9_+\-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,6}"
)


def validate_email(address):
    """Вернуть пару (корректен, причина ошибки)."""
    if not address:
        return False, "Пустой адрес"
    if any(char.isspace() for char in address):
        return False, "Адрес содержит пробельные символы"
    if address.count("@") != 1:
        return False, "Адрес должен содержать ровно один символ @"
    local, domain = address.split("@")
    if not local:
        return False, "Нет локальной части"
    if not re.fullmatch(r"[A-Za-z0-9._+\-]+", local):
        return False, "Недопустимые символы в локальной части"
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False, "Неправильное расположение точек в локальной части"
    if not domain:
        return False, "Нет доменной части"
    if domain.startswith(".") or domain.endswith("."):
        return False, "Домен начинается или заканчивается точкой"
    if ".." in domain:
        return False, "Две точки подряд в домене"
    if "." not in domain:
        return False, "Нет точки в домене"
    if not re.fullmatch(r"[A-Za-z0-9.-]+", domain):
        return False, "Недопустимые символы в домене"
    if any(part.startswith("-") or part.endswith("-")
           for part in domain.split(".")):
        return False, "Часть домена начинается или заканчивается дефисом"
    if not re.fullmatch(r"[A-Za-z]{2,6}", domain.rsplit(".", 1)[1]):
        return False, "Окончание домена должно содержать 2–6 латинских букв"
    if not EMAIL_PATTERN.fullmatch(address):
        return False, "Адрес не соответствует формату"
    return True, ""
