from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as BaseModelPydantic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseModel, User


class CRUDBase:
    """Базовый класс реализациия CRUD операций."""
    def __init__(self, model: BaseModel) -> None:
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> BaseModel:
        """Получение записи."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> list[BaseModel]:
        """Возвращает все записей."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: BaseModelPydantic,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> BaseModel:
        """Создание записи."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: BaseModel,
            obj_in: BaseModelPydantic,
            session: AsyncSession,
    ) -> BaseModel:
        """Обновление записи."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: BaseModel,
            session: AsyncSession,
    ) -> BaseModel:
        """Удаление записи."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_no_close(self, session: AsyncSession) -> list[BaseModel]:
        """Возвращает все не закрытые записи."""
        no_close_objs = await session.execute(select(self.model).where(
            self.model.fully_invested.is_(False)
        ))
        no_close_objs = no_close_objs.scalars().all()
        return no_close_objs