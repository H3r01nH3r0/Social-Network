import os
import datetime
from typing import List

from fastapi import UploadFile

from app.auth.models import User
from app.auth.service import AuthService
from app.posts.schemas import Post, Author
from app.posts.service import PostService
import base64


def to_base64(file_path: str):
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read())
        return content


async def get_created_post(post, author) -> Post:
    if post.image_path:
        image = to_base64(post.image_path)
    else:
        image = None

    post_to_add = Post(
        id=post.id,
        title=post.title,
        text=post.text,
        image_path=image,
        author=Author(
            id=author.id,
            first_name=author.first_name,
            last_name=author.last_name
        ),
        publication_date=post.publication_date,
        like_count=post.like_count,
        is_liked=False,
        is_owner=True
    )
    return post_to_add


async def get_all_posts(
        skip: int,
        limit: int,
        user: User,
        post_service: PostService,
        user_service: AuthService,
) -> List[Post]:
    result = []
    posts = await post_service.get_all(skip, limit)
    for post in posts:
        if post.image_path:
            image = to_base64(post.image_path)
        else:
            image = None
        is_owner = True if user.id == post.author_id else False
        author = await user_service.get_by_id(post.author_id)
        is_liked = await post_service.is_liked(post.id, user.id)
        post_to_add = Post(
            id=post.id,
            title=post.title,
            text=post.text,
            image_path=image,
            author=Author(
                id=author.id,
                first_name=author.first_name,
                last_name=author.last_name
            ),
            publication_date=post.publication_date,
            like_count=post.like_count,
            is_liked=is_liked,
            is_owner=is_owner
        )
        result.append(post_to_add)
    return result


async def download_file(file: UploadFile, username: str) -> str:
    home = os.getcwd()
    # Change directory
    os.chdir("images")
    if username not in os.listdir(os.getcwd()):
        os.mkdir(username)
    os.chdir(username)
    # Generate file name
    upload_at = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{upload_at}{file.filename}"
    # Save file to local storage
    with open(filename, "wb") as file_create:
        file_create.write(await file.read())
    # Returns to home directory
    os.chdir(home)
    # Save file path
    path = f"./images/{username}/{filename}"
    return path
