from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, Form

from app.auth.schemas import User
from app.auth.service import get_current_user, AuthService
from app.posts.schemas import Post, PostCreate, PostUpdate
from app.posts.service import PostService
from app.posts.utils import download_file, get_all_posts, get_created_post

router = APIRouter(
    prefix="/wall",
    tags=["Content"]
)


@router.get("/", response_model=List[Post])
async def get_all(
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(),
        user_service: AuthService = Depends()
):
    """
    Get first ten posts from database.
    Change skip or/and limit params to see more.
    """
    # need to do this using join instead one more calling to AuthService
    result = await get_all_posts(skip, limit, user, post_service, user_service)
    return result


@router.post("/create")
async def create(
        file: UploadFile | None = None,
        title: str = Form(...),
        text: str = Form(...),
        user: User = Depends(get_current_user),
        service: PostService = Depends()
):
    """
    Create a new single post.
    """
    path = (await download_file(file, user.email)) if file else None
    new_post = PostCreate(title=title, text=text, image_path=path)
    created_post = await service.create(new_post, user_id=user.id)
    result = await get_created_post(created_post, user)
    return result


@router.patch("/update/{post_id}", status_code=status.HTTP_200_OK)
async def update(
        post_id: int,
        file: UploadFile | None = None,
        title: str = Form(default=None),
        text: str = Form(default=None),
        user: User = Depends(get_current_user),
        service: PostService = Depends(),
):
    """
    Update a single post.
    """
    # Uploading files realized on backend, but not in frontend,
    # So file param is usually empty
    path = (await download_file(file, user.id)) if file else None
    post_data = PostUpdate(title=title, text=text, image_path=path)
    await service.update(post_data, post_id, user.id)
    return {"status": "UPDATED"}


@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        post_id: int,
        user: User = Depends(get_current_user),
        service: PostService = Depends(),
):
    """
    Delete a single post.
    """
    await service.delete(user.id, post_id)
    return {"status": "DELETED"}


@router.put("/like/{post_id}", status_code=status.HTTP_200_OK)
async def like(
        post_id: int,
        user: User = Depends(get_current_user),
        service: PostService = Depends()
):
    """
    Change like status.
    Like if user have not already like the post, else dislike.
    """
    await service.update_like_count(post_id, user.id)
    return {"status": "LIKED"}
