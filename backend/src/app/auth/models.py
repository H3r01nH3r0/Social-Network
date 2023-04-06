from datetime import datetime
from datetime import date
import sqlalchemy as sa
from src.app.database import Base


class User(Base):
    __tablename__ = "user"

    id: int = sa.Column(sa.Integer, primary_key=True)
    email: str = sa.Column(sa.String, unique=True, nullable=False)
    hashed_password: str = sa.Column(sa.String, nullable=False)
    registration_date: datetime = sa.Column(sa.TIMESTAMP, default=datetime.utcnow)
    first_name: str = sa.Column(sa.String, nullable=False)
    last_name: str = sa.Column(sa.String, nullable=False)
    birth_date: date = sa.Column(sa.Date, nullable=False, default=date.today)

