from typing import List, Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
   title: str
   description: Optional[str] = None


class ArticleCreate(ArticleBase):
   pass


class ArticleUpdate(ArticleBase):
   pass


class ArticleDelete(ArticleBase):
   id: int


class Article(ArticleBase):
   id: int
   owner_id: int

   class Config:
      orm_mode = True


class UserBase(BaseModel):
   email: str
   name: str


class UserCreate(UserBase):
   password: str


class UserUpdate(UserBase):
   pass


class UserDelete(UserBase):
   id: int


class User(UserBase):
   id: int
   is_active: bool
   articles: List[Article] = []

   class Config:
       orm_mode = True