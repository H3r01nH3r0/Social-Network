import sqlalchemy as sa
from datetime import datetime
from src.app.database import Base


class Post(Base):
    __tablename__ = "post"

    id: int = sa.Column(sa.Integer, primary_key=True)
    author_id: int = sa.Column(sa.Integer, sa.ForeignKey("user.id"))
    publication_date: datetime = sa.Column(sa.TIMESTAMP, default=datetime.utcnow)
    title: str = sa.Column(sa.String, nullable=False)
    text: str = sa.Column(sa.String, nullable=False)
    image_path: str = sa.Column(sa.String)
    like_count: int = sa.Column(sa.Integer, nullable=False, default=0)


class Like(Base):
    __tablename__ = "like"

    id: int = sa.Column(sa.Integer, primary_key=True)
    post_id: int = sa.Column(sa.Integer, sa.ForeignKey("post.id"))
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("user.id"))

