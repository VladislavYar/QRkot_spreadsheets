from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import BaseModel


async def investing_projects(obj: BaseModel, crud: CRUDBase,
                             session: AsyncSession) -> None:
    """Инвестирует пожертвования(е) в проект(ы)."""
    objs_no_close = await crud.get_no_close(session)
    if not objs_no_close:
        return obj
    full_amount = obj.full_amount
    invested_amount = 0
    for obj_no_close in objs_no_close:
        amount = obj_no_close.full_amount - obj_no_close.invested_amount
        if full_amount > amount:
            full_amount -= amount
            invested_amount += amount
            obj_no_close.invested_amount = obj_no_close.full_amount
            obj_no_close.fully_invested = True
            obj_no_close.close_date = dt.now()
            session.add(obj_no_close)
        elif full_amount < amount:
            invested_amount = obj.full_amount
            obj.fully_invested = True
            obj.close_date = dt.now()
            obj_no_close.invested_amount += full_amount
            session.add(obj_no_close)
            break
        else:
            invested_amount = obj.full_amount
            obj.fully_invested = True
            obj.close_date = dt.now()
            obj_no_close.invested_amount = obj_no_close.full_amount
            obj_no_close.fully_invested = True
            obj_no_close.close_date = dt.now()
            session.add(obj_no_close)
            break
    obj.invested_amount = invested_amount
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
