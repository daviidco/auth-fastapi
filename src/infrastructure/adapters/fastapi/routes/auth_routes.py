from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.application.use_cases.auth_uc import UserUseCases
from src.domain.ports.ISettingRepository import ISettingRepository
from src.domain.ports.IUserRepository import IUserRepository
from src.infrastructure.adapters.db.database import get_db
from src.infrastructure.adapters.db.repositories.sql_alchemy_user_repository import (  # noqa: E501
    SQLAlchemyUserRepository,
)  # noqa: E501
from src.infrastructure.adapters.fastapi.oauth2 import oauth2_scheme
from src.infrastructure.adapters.fastapi.schemas.user_schemas import (
    TokenSchema,
)
from src.infrastructure.config.setting_repository import SettingRepository
from src.infrastructure.config.settings import get_settings

router = APIRouter()
settings = get_settings()


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


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> TokenSchema:
    token = await user_use_cases.login_user(
        form_data.username, form_data.password
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenSchema(
        access_token=token.access_token, token_type=token.token_type
    )


@router.post("/token/create-refresh", response_model=TokenSchema)
async def create_refresh_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> TokenSchema:
    refresh_token_data = {"sub": form_data.username}
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = user_use_cases.create_refresh_token(
        refresh_token_data, expires_delta=refresh_token_expires
    )
    return TokenSchema(access_token=refresh_token, token_type="bearer")


@router.post("/token/refresh", response_model=TokenSchema)
async def refresh_access_token(
    refresh_token: str = Depends(oauth2_scheme),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> TokenSchema:
    new_access_token = await user_use_cases.refresh_access_token(refresh_token)
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenSchema(access_token=new_access_token, token_type="bearer")
