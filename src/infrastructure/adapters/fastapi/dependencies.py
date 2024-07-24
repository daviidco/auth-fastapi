from fastapi import Depends

from src.application.use_cases.auth_uc import UserUseCases
from src.domain.ports.ISettingRepository import ISettingRepository
from src.domain.ports.IUserRepository import IUserRepository
from src.infrastructure.adapters.db.database import get_db
from src.infrastructure.adapters.db.repositories.sql_alchemy_user_repository import (  # noqa: E501
    SQLAlchemyUserRepository,
)
from src.infrastructure.config.setting_repository import SettingRepository
from src.infrastructure.config.settings import get_settings


def get_user_repository(db_session=Depends(get_db)):
    return SQLAlchemyUserRepository(db_session)


def get_setting_repository() -> SettingRepository:
    settings = get_settings()
    return SettingRepository(settings)


def get_user_use_cases(
    user_repository: IUserRepository = Depends(get_user_repository),
    setting_repository: ISettingRepository = Depends(get_setting_repository),
) -> UserUseCases:
    return UserUseCases(user_repository, setting_repository)
