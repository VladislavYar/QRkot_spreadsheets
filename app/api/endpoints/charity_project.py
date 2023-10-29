from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate,
                                validate_charity_project_delete,
                                validate_charity_project_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import investing_projects

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Отдаёт все проекты."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser), ),
    response_model=CharityProjectDB
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создание проекта. Только для superuser-a."""
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(charity_project,
                                                        session)
    await investing_projects(charity_project, donation_crud, session)
    return charity_project


@router.delete(
    '/{project_id}',
    dependencies=(Depends(current_superuser), ),
    response_model=CharityProjectDB
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаление проекта. Только для superuser-a."""
    charity_project = await validate_charity_project_delete(project_id,
                                                            session)
    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    '/{project_id}',
    dependencies=(Depends(current_superuser), ),
    response_model=CharityProjectDB
)
async def patch_charity_project(
    project_id: int,
    charity_project_update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление проекта. Только для superuser-a."""
    charity_project = (
        await validate_charity_project_update(project_id,
                                              charity_project_update_data,
                                              session)
    )
    return await charity_project_crud.update(charity_project,
                                             charity_project_update_data,
                                             session)