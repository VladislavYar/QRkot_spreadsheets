from datetime import datetime as dt
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.orm import validates

from app.core.constants import REQUIRED, SUM_MORE_ZERO
from app.core.db import Base


class BaseModel(Base):
    """Базовая модель."""
    __abstract__ = True
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime)
    fully_invested = Column(Boolean, default=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)

    @validates('full_amount')
    def validate_full_amount(self, key: str, value: Optional[int]) -> int:
        """Валидация поля full_amount."""
        if value is None:
            raise TypeError(REQUIRED)
        if value <= 0:
            raise ValueError(SUM_MORE_ZERO)
        return value