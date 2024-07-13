from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.domain.entities.user_entities import User, UserCreate
from src.domain.ports.IUserRepository import IUserRepository
from src.infrastructure.adapters.db.models.user import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, user: UserCreate) -> Optional[User]:
        db_user = UserModel(
            username=user.username,
            hashed_password=user.password,
            email=user.email,
        )
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return User(
            username=db_user.username,
            email=db_user.email,
            full_name=db_user.full_name,
            disabled=db_user.disabled,
        )

    async def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user_model = (
            self.db_session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
        if user_model:
            return User(
                username=user_model.username,
                email=user_model.email,
                full_name=user_model.full_name,
                disabled=user_model.disabled,
            )
        return None

    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[User]:
        user_model = (
            self.db_session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )

        if user_model and await self.verify_password(
            password, user_model.hashed_password
        ):
            return User(
                username=user_model.username,
                email=user_model.email,
                full_name=user_model.full_name,
                disabled=user_model.disabled,
            )
        return None

    async def update_user(self, user: User) -> None:
        db_user = (
            self.db_session.query(UserModel)
            .filter(UserModel.username == user.username)
            .first()
        )
        if db_user:
            db_user.email = user.email
            db_user.full_name = user.full_name
            db_user.disabled = user.disabled
            self.db_session.commit()

    async def delete_user(self, username: str) -> None:
        db_user = (
            self.db_session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
        if db_user:
            self.db_session.delete(db_user)
            self.db_session.commit()
