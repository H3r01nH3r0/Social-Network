import os
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from src.app.posts import models as tables
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.posts.schemas import PostCreate, PostUpdate


class PostService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create(self, post_data: PostCreate, user_id: int) -> tables.Post:
        """Add a new single post into database."""
        new_post = tables.Post(author_id=user_id, **post_data.dict())
        try:
            self.session.add(new_post)
            await self.session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create post...")
        return new_post

    async def get_by_id(self, post_id: int) -> tables.Post:
        """Get post by id from database."""
        stmt = select(tables.Post).where(tables.Post.id == post_id)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return result

    async def get_all(self, skip: int, limit: int) -> List[tables.Post]:
        """Get list of posts from database."""
        stmt = (
            select(tables.Post)
            .offset(skip)
            .limit(limit)
            .order_by(
                tables.Post.id.desc(),
            )
        )
        result = await self.session.execute(stmt)
        result = result.scalars().all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts")
        return result

    async def update(self, post_data: PostUpdate, post_id: int, user_id: int) -> None:
        """Patch a single post."""
        post = await self.get_by_id(post_id)
        if post.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        try:
            for field, value in post_data:
                if not value:
                    continue
                setattr(post, field, value)
            await self.session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update post...")

    async def is_liked(self, post_id: int, user_id: int) -> bool:
        return bool(await self.__is_liked(post_id, user_id))

    async def __is_liked(self, post_id: int, user_id: int) -> tables.Like:
        stmt = select(tables.Like).where((tables.Like.post_id == post_id) & (tables.Like.user_id == user_id))
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        return result

    async def __user_like(self, post_id: int, user_id: int) -> None:
        result = tables.Like(
            post_id=post_id,
            user_id=user_id
        )
        self.session.add(result)
        await self.session.flush()

    async def __user_dislike(self, post: tables.Like) -> None:
        await self.session.delete(post)
        await self.session.flush()

    async def update_like_count(self, post_id: int, user_id: int) -> None:
        is_liked = await self.__is_liked(post_id, user_id)
        post = await self.get_by_id(post_id)
        if is_liked:
            post.like_count -= 1
            await self.__user_dislike(is_liked)
        else:
            post.like_count += 1
            await self.__user_like(post_id, user_id)
        await self.session.commit()

    async def __delete_likes(self, post_id: int) -> None:
        """
        Delete all entries in Like table
        """
        stmt = delete(tables.Like).where(tables.Like.post_id == post_id)
        await self.session.execute(stmt)
        await self.session.flush()

    @staticmethod
    def delete_file(path: str) -> None:
        """Delete media associated with the post"""
        os.remove(path)

    async def delete(self, user_id: int, post_id: int) -> None:
        """
        Delete a post from database.
        Also delete all entries in Like table and removes all media associated with the post
        """
        post = await self.get_by_id(post_id)
        if post.image_path:
            self.delete_file(post.image_path)
        if post.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        if post.like_count < 1:
            await self.session.delete(post)
            await self.session.commit()
        else:
            await self.__delete_likes(post_id)
            await self.session.delete(post)
            await self.session.commit()
