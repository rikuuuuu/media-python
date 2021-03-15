from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp, now

from . import models
from . import schemas


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate, userID: int):
    db_item = models.Article(title=article.title, description=article.description, owner_id=userID)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_article(db: Session, article: schemas.ArticleUpdate):
    article = db.query(models.Article).filter(models.Article.id == int(article.id)).first()
    article.title = article.title
    article.description = article.description
    # article.updated_at = datetime.now
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article: schemas.ArticleDelete):
    db.query(models.Article).filter(models.Article.id == int(article.id)).delete()
    db.commit()
    return