from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field
from pydantic.types import PositiveInt

from app.core.constants import MAX_LEN_NAME, MIN_LEN_DESCRIPTION, MIN_LEN_NAME


class CharityProjectBase(BaseModel):
    """Базовая схема charity_project."""
    name: str = Field(..., min_length=MIN_LEN_NAME, max_length=MAX_LEN_NAME)
    description: str = Field(..., min_length=MIN_LEN_DESCRIPTION)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Cхема создания charity_project."""
    pass


class CharityProjectUpdate(CharityProjectBase):
    """Cхема обновления charity_project."""
    name: Optional[str] = Field(None, min_length=MIN_LEN_NAME,
                                max_length=MAX_LEN_NAME)
    description: Optional[str] = Field(None, min_length=MIN_LEN_DESCRIPTION)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    """Cхема вывода данных из БД charity_project."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True