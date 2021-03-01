from fastapi import Depends, FastAPI, HTTPException
from app.database import SessionLocal

from . import user_crud, article_crud

from pb import entity_article_pb2, entity_admin_user_pb2


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


class AdminUserService(object):
    def GetMe(self, context, user):
        db = SessionLocal()
        res = user_crud.get_user(db=db, user_id=user.id)
        return entity_admin_user_pb2.AdminUser(
            id=str(res.id),
            name=res.name,
            email=res.email,
        )

    def Create(self, context, user):
        db = SessionLocal()
        res = user_crud.create_user(db=db, user=user)
        return entity_admin_user_pb2.AdminUser(
            id=str(res.id),
            name=res.name,
            email=res.email,
        )

    def Update(self, context, user):
        db = SessionLocal()
        res = user_crud.update_user(db=db, item=user)
        if res is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return entity_admin_user_pb2.AdminUser(
            id=str(res.id),
            name=res.name,
            email=res.email,
        )

    def Delete(self, context, user):
        db = SessionLocal()
        user_crud.delete_user(db=db, item=user)
        return entity_article_pb2.Empty()


class ArticleService(object):
    def Get(self, context, article):
        db = SessionLocal()
        res = article_crud.get_article(db=db, article_id=int(article.id))
        if res is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return entity_article_pb2.Article(
            id=str(res.id),
            title=res.title,
            description=res.description,
            userID=str(res.owner_id),
            createdAt=str(res.created_at),
            updatedAt=str(res.updated_at)
        )

    def GetAll(self, context, item):
        db = SessionLocal()
        resList = article_crud.get_articles(db=db)
        articleList: entity_article_pb2.ArticleList = []

        for res in resList:
            art: entity_article_pb2.Article = entity_article_pb2.Article(
                id=str(res.id),
                title=res.title,
                description=res.description,
                userID=str(res.owner_id),
                createdAt=str(res.created_at),
                updatedAt=str(res.updated_at)
            )

            articleList.append(art)

        return entity_article_pb2.ArticleList(
                items=articleList
            )

    def Create(self, context, article):
        db = SessionLocal()
        res = article_crud.create_article(db=db, item=article)
        return entity_article_pb2.Article(
            id=str(res.id),
            title=res.title,
            description=res.description,
            userID=str(res.owner_id),
            createdAt=str(res.created_at),
            updatedAt=str(res.updated_at)
        )

    def Update(self, context, article):
        db = SessionLocal()
        res = article_crud.update_article(db=db, item=article)
        if res is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return entity_article_pb2.Article(
            id=str(res.id),
            title=res.title,
            description=res.description,
            userID=str(res.owner_id),
            createdAt=str(res.created_at),
            updatedAt=str(res.updated_at)
        )

    def Delete(self, context, article):
        db = SessionLocal()
        article_crud.delete_article(db=db, item=article)
        return entity_article_pb2.Empty()