from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


@dataclass
class UserCreate:
    username: str
    password: str
    email: Optional[str] = None


@dataclass
class Token:
    access_token: str
    token_type: str


@dataclass
class TokenData:
    username: str | None = None
