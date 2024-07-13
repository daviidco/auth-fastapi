# user_repository.py

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user_entities import User, UserCreate


class IUserRepository(ABC):

    @abstractmethod
    async def verify_password(self, plain_password, hashed_password):
        pass

    @abstractmethod
    async def get_password_hash(self, password):
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, user: UserCreate) -> Optional[User]:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    async def delete_user(self, username: str) -> None:
        pass
