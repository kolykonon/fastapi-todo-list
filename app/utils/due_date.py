from datetime import datetime, date, timezone
from typing import Optional, Union


class DueDate:
    def __init__(self, value: Optional[Union[datetime, date, str]]):
        self._value = self._parse(value) if value else None

    def _parse(self, value: Optional[Union[datetime, date, str]]) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, datetime.max.time())
        if isinstance(value, str):
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y %H:%M", "%d.%m.%Y"]:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Неправильный формат даты {value}")
        raise ValueError(f"Неправильный тип даты {type(value)}")

    @property
    def value(self) -> Optional[datetime]:
        return self._value

    @property
    def is_overdue(self) -> bool:
        if not self._value:
            return False
        return datetime.now(timezone.utc) > self.value

    @property
    def days_until(self) -> Optional[int]:
        if not self._value:
            return None
        delta = self._value - datetime.now(timezone.utc)
        return delta.days

    @property
    def days_overdue(self) -> Optional[int]:
        if not self._value:
            return None
        overdue = datetime.now(timezone.utc) - self._value
        return overdue.days

    def __str__(self):
        if not self._value:
            return "Нет срока истечения задачи"
        return self._value.strftime("%d.%m.%Y %H:%M")
