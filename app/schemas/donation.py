from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra
from pydantic.types import PositiveInt


class DonationBase(BaseModel):
    """Базовая схема donation."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Cхема создания donation."""
    pass


class DonationDB(DonationBase):
    """Cхема вывода данных из БД для обычного user-a donation."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperuserDB(DonationDB):
    """Cхема вывода данных из БД для superuser-a donation."""
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]