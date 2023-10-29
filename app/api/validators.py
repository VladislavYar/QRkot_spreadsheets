from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (NO_DELETE_PROJECT_INVESTED_AMOUNT,
                                NO_INVESTED_AMOUNT_MORE_FULL_AMOUNT,
                                NO_PROJECT, NO_UNIQUE_NAME,
                                NO_UPDATE_CLOSE_PROJECT)
from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяет на наличие записи в БД."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NO_PROJECT
        )
    return charity_project


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет на дубликат имени в БД."""
    charity_project_id = (
        await charity_project_crud.get_charity_project_id_by_name(
            charity_project_name, session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_UNIQUE_NAME,
        )


async def validate_charity_project_update(
    project_id: int,
    charity_project_update_data: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Валидация данных при обновлении записи в БД."""
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project_update_data.name is not None:
        await check_name_duplicate(charity_project_update_data.name, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_UPDATE_CLOSE_PROJECT,
        )
    if (charity_project_update_data.full_amount and
       charity_project.invested_amount >
       charity_project_update_data.full_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_INVESTED_AMOUNT_MORE_FULL_AMOUNT,
        )
    return charity_project


async def validate_charity_project_delete(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Валидация данных при удалении записи из БД."""
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_DELETE_PROJECT_INVESTED_AMOUNT,
        )
    return charity_project