from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    """Класс реализациия CRUD операций для таблицы donation."""
    async def get_by_user(self, user: int,
                          session: AsyncSession) -> list[Donation]:
        """Получение записей с фильтрацией по user-у."""
        donations = await session.execute(select(self.model).where(
            self.model.user_id == user.id
        ))
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)