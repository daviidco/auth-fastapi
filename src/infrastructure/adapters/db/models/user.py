from sqlalchemy import Boolean, Column, Integer, String

from src.infrastructure.adapters.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    disabled = Column(Boolean, default=False, index=True)
    hashed_password = Column(
        String, nullable=False
    )  # Nuevo campo para la contraseña hasheada
