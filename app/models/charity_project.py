from typing import Optional

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates

from app.core.constants import (DESCRIPTION_NO_LESS_MIN_LEN_DESCRIPTION,
                                MAX_LEN_NAME, MIN_LEN_DESCRIPTION,
                                MIN_LEN_NAME, NAME_LEN_MIN_MAX, REQUIRED)
from app.models import BaseModel


class CharityProject(BaseModel):
    """Модель таблицы charityproject."""
    name = Column(String(MAX_LEN_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    @validates('description')
    def validate_description(self, key: str, value: Optional[str]) -> str:
        """Валидация поля description."""
        if value is None:
            raise TypeError(REQUIRED)
        if len(value) < MIN_LEN_DESCRIPTION:
            raise ValueError(DESCRIPTION_NO_LESS_MIN_LEN_DESCRIPTION)
        return value

    @validates('name')
    def validate_name(self, key: str, value: Optional[str]) -> str:
        """Валидация поля name."""
        if value is None:
            raise TypeError(REQUIRED)
        string_length = len(value)
        if string_length == MIN_LEN_NAME or string_length > MAX_LEN_NAME:
            raise ValueError(NAME_LEN_MIN_MAX)
        return value