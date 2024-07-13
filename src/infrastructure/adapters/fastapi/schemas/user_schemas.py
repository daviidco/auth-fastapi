from pydantic import BaseModel, EmailStr, field_validator


class UserCreateSchema(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None

    @field_validator("password")
    def check_password(cls, value):
        # convert the password to a string if it is not already
        value = str(value)
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must have at least one uppercase letter"
            )
        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must have at least one lowercase letter"
            )
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
