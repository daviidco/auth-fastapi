from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.auth_uc import UserUseCases
from src.infrastructure.adapters.fastapi.dependecies import get_user_use_cases
from src.infrastructure.adapters.fastapi.oauth2 import oauth2_scheme
from src.infrastructure.adapters.fastapi.schemas import (
    user_schemas as schemas_user,
)
from src.infrastructure.adapters.fastapi.schemas.user_schemas import UserSchema

router = APIRouter()

prefix_auth = "/auth"


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        current_user = await user_use_cases.get_current_active_user(token)
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )
        return current_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/users/me/items/")
async def read_own_items(
    token: str = Depends(oauth2_scheme),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:

        current_user = await user_use_cases.get_current_active_user(token)
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )
        items = user_use_cases.get_user_items(current_user)
        return items
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/register", response_model=schemas_user.UserSchema)
async def register(
    user: schemas_user.UserCreateSchema,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
):
    new_user = await user_use_cases.register_user(
        user.username, user.password, user.email
    )
    return new_user
