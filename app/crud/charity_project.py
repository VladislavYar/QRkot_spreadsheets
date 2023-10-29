from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс реализациия CRUD операций для таблицы сharityproject."""
    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Отдаёт id записи, найденную по имени."""
        charity_project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == charity_project_name
            )
        )
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id
    
    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        """
        Возвращает закрытые проекты,
        отсортированные по времени сбора пожертвований.
        """
        close_projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(True)
            ).order_by(
                func.julianday(self.model.close_date) -
                func.julianday(self.model.create_date)
            )
        )
        return close_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)