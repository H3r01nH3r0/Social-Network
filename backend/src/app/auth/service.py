from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import models
from app.auth.schemas import CreateUser, Token, User, UpdateUser, UserValidate
from app.database import get_async_session
from app.settings import settings

from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/sign-in")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return await AuthService.validate_token(token)


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    @classmethod
    async def create_token(cls, user: models.User) -> Token:
        payload = {
            "sub": user.email,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_expiration)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return Token(access_token=encoded_jwt)

    @classmethod
    async def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "www-Authenticate": 'Bearer'
            }
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise exception
        except JWTError:
            raise exception

        user_data = payload.get("user")

        try:
            user = UserValidate.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    async def create(self, user_data: CreateUser) -> Token:
        user = models.User(
            email=user_data.email,
            hashed_password=await self.hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            birth_date=user_data.birth_date
        )
        try:
            self.session.add(user)
            await self.session.commit()
            return await self.create_token(user)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    async def get_by_id(self, user_id: int) -> models.User:
        stmt = (
            select(models.User)
            .where(models.User.id == user_id)
        )
        user = (await self.session.execute(stmt)).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def get_by_username(self, username: str) -> models.User:
        stmt = (
            select(models.User)
            .where(models.User.email == username)
        )
        user = (await self.session.execute(stmt)).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def authenticate(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "www-Authenticate": 'Bearer'
            }
        )
        try:
            user = await self.get_by_username(username)
        except HTTPException:
            raise exception

        if not (await self.verify_password(password, user.hashed_password)):
            raise exception

        return await self.create_token(user)

    async def change_password(self, old_password: str, new_password: str, user_id: int) -> models.User:
        user = await self.get_by_id(user_id)
        if not (await self.verify_password(old_password, user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
        hashed_password = await self.hash_password(new_password)
        user.hashed_password = hashed_password
        await self.session.commit()
        return user

    async def update(self, user_data: UpdateUser, user_id: int) -> Token:
        user = await self.get_by_id(user_id)
        try:
            for field, value in user_data:
                setattr(user, field, value)
            await self.session.commit()
            return await self.create_token(user)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unavailable username or email")

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        await self.session.delete(user)
        await self.session.commit()
