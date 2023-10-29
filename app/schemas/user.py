from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема чтения user."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания user."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления user."""
    pass
