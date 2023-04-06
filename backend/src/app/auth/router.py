from fastapi import APIRouter, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schemas import Token, CreateUser, User, UpdateUser
from app.auth.service import AuthService, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(
        user_data: CreateUser,
        service: AuthService = Depends(),
):
    await service.create(user_data)
    return {"status": "CREATED"}


@router.post("/sign-in", response_model=Token)
async def sign_in(
        user_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return await service.authenticate(
        user_data.username,
        user_data.password
    )


@router.get("/me", response_model=User)
async def get_me(
        user: User = Depends(get_current_user),
        service: AuthService = Depends()
):
    return await service.get_by_id(user.id)


@router.get("/{user_id}", response_model=User, dependencies=[Depends(get_current_user)])
async def get_by_id(
        user_id: int,
        service: AuthService = Depends(),
):
    return await service.get_by_id(user_id)


@router.patch("/update", status_code=status.HTTP_200_OK)
async def update(
        user_data: UpdateUser,
        user: User = Depends(get_current_user),
        service: AuthService = Depends(),
):
    return await service.update(user_data, user.id)


@router.patch("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
        user: User = Depends(get_current_user),
        old_password: str = Form(...),
        new_password: str = Form(...),
        service: AuthService = Depends(),
):
    await service.change_password(old_password, new_password, user.id)
    return {"status": "UPDATED"}


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        user: User = Depends(get_current_user),
        service: AuthService = Depends(),
):
    await service.delete(user.id)
    return {"status": "DELETED"}
