from datetime import date, datetime

from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class CreateUser(BaseUser):
    password: str
    first_name: str
    last_name: str
    birth_date: date


class UpdateUser(BaseUser):
    pass


class UserValidate(BaseUser):
    id: int
    first_name: str
    last_name: str


class User(BaseUser):
    id: int
    registration_date: datetime
    first_name: str
    last_name: str
    birth_date: date

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
