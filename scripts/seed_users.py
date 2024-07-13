import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.infrastructure.adapters.db.database import Base, SessionLocal, engine
from src.infrastructure.adapters.db.models.user import User

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


def seed_users(db: Session, username: str, email: str, hashed_password: str):
    new_user = User(
        username=username, email=email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def insert_initial_users(db: Session):
    users_to_insert = [
        {
            "username": "johndoe",
            "email": "usuario1@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # noqa: E501
            "full_name": "John Doe",
        },
        {
            "username": "daviidco",
            "email": "usuario2@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # noqa: E501
            "full_name": "David Cortés",
        },
    ]

    for user_data in users_to_insert:
        try:
            seed_users(
                db,
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=user_data["hashed_password"],
            )
        except IntegrityError:
            db.rollback()
            print(f"User {user_data['email']} already exists.")


def main():
    # Crear las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        insert_initial_users(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
