from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import DateTime

from .database import Base, engine


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    name = Column(String(50), index=True, nullable=True, unique=False)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(500), nullable=True)
    articles = relationship("Article", back_populates="owner")


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    description = Column(String(1000), index=True)
    thumbnailURL = Column(String(100), index=True, nullable=True, unique=False)
    created_at = Column(
        DateTime, default=datetime.now(), server_default=current_timestamp()
    )
    updated_at = Column(
        DateTime, default=datetime.now(), server_onupdate=current_timestamp()
    )
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="articles")


Base.metadata.create_all(engine)
