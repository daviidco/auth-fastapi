from datetime import datetime, timedelta
from typing import Optional, Union

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from src.domain.entities.user_entities import Token, User, UserCreate
from src.domain.ports.ISettingRepository import ISettingRepository
from src.domain.ports.IUserRepository import IUserRepository
from src.infrastructure.config.settings import (
    get_settings,
)  # Importar las configuraciones

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserUseCases:
    def __init__(
        self,
        user_repository: IUserRepository,
        setting_repository: ISettingRepository,
    ):
        self.user_repository = user_repository
        self.setting_repository = setting_repository
        self.secret_key = setting_repository.get_secret_key()
        self.encryption_algorithm = (
            setting_repository.get_encryption_algorithm()
        )
        self.access_token_expire_minutes = (
            setting_repository.get_access_token_expire_minutes()
        )
        self.refresh_token_expire_days = (
            setting_repository.get_refresh_token_expire_days()
        )

    async def register_user(
        self, username: str, password: str, email: str | None
    ) -> Optional[User]:
        user_create = UserCreate(username, password, email)
        hashed_password = await self.user_repository.get_password_hash(
            user_create.password
        )
        user_create.password = hashed_password
        return await self.user_repository.create_user(user_create)

    async def verify_password(self, plain_password, hashed_password):
        return self.user_repository.verify_password(
            plain_password, hashed_password
        )

    async def get_password_hash(self, password):
        return self.user_repository.get_password_hash(password)

    async def get_current_user(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.encryption_algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                return None  # Devuelve None si no hay username en el payload
            # To get toke info token_data = TokenData(username=username)
        except InvalidTokenError:
            return None  # Devuelve None si hay un error en el token

        user = await self.user_repository.get_user_by_username(username)
        return user

    async def get_current_active_user(self, token: str) -> Optional[User]:
        current_user = await self.get_current_user(token)
        if current_user is None:
            return None  # Devuelve None si no se pudo obtener el usuario
        if current_user.disabled:
            raise ValueError(
                "Usuario inactivo"
            )  # Lanza una excepción si el usuario está deshabilitado
        return current_user

    async def login_user(
        self, username: str, password: str
    ) -> Optional[Token]:
        user: User = await self.user_repository.authenticate_user(
            username, password
        )
        if user:
            access_token = self.create_access_token(
                data={"sub": user.username}
            )
            return Token(access_token=access_token, token_type="bearer")
        return None

    def get_user_items(self, user: User) -> list:
        # Implementa la lógica para obtener los ítems del usuario
        return [{"item_id": "Foo", "owner": user.username}]

    def create_access_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.encryption_algorithm
        )
        return encoded_jwt

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=self.refresh_token_expire_days
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.encryption_algorithm
        )
        return encoded_jwt

    async def refresh_access_token(
        self, refresh_token: str
    ) -> Union[str, None]:
        try:
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.encryption_algorithm],
            )
            username: str = payload.get("sub")
            if username is None:
                return None
        except InvalidTokenError:
            return None

        user = await self.user_repository.get_user_by_username(username)
        if user is None:
            return None

        access_token = self.create_access_token(data={"sub": username})
        return access_token
