from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models import BaseModel


class Donation(BaseModel):
    """Модель таблицы donation."""
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)