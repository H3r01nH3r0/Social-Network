from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    image_path: str | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: str | None = None
    text: str | None = None


class Author(BaseModel):
    id: int
    first_name: str
    last_name: str


class Post(PostBase):
    id: int
    author: Author
    publication_date: datetime
    like_count: int
    is_liked: bool = False
    is_owner: bool = False

    class Config:
        orm_mode = True
