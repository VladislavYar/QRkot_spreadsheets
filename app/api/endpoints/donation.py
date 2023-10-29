from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationDB,
                                  DonationSuperuserDB)
from app.services.investment import investing_projects

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser), ),
    response_model=list[DonationSuperuserDB]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получение всех пожертвований. Только для superuser-a."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model_exclude_none=True,
    response_model=DonationDB
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Создание пожертвования. Только для зарегестрированного пользователя."""
    donation = await donation_crud.create(donation, session, user)
    await investing_projects(donation, charity_project_crud, session)
    return donation


@router.get('/my',
            response_model_exclude_none=True,
            response_model=list[DonationDB]
            )
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получения личных пожертвований.
    Только для зарегестрированного пользователя.
    """
    donations = await donation_crud.get_by_user(user, session)
    return donations