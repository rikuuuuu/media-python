from typing import List, Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    thumbnailURL: str


class ArticleGet(BaseModel):
    id: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    id: str


class ArticleDelete(BaseModel):
    id: str


class Article(ArticleBase):
    id: str
    userID: str
    createdAt: str
    updatedAt: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserGet(BaseModel):
    id: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str


class UserDelete(BaseModel):
    id: str


class User(UserBase):
    id: int
    name: str
    is_active: bool
    articles: List[Article] = []

    class Config:
        orm_mode = True
