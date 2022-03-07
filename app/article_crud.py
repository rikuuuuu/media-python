# from datetime import datetime
import os
from os import getenv

# from sqlalchemy.sql.functions import current_timestamp, now
import boto3
from dotenv import load_dotenv
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

load_dotenv()

from logging import DEBUG, StreamHandler, getLogger

from . import models, schemas

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate, userID: int):
    db_item = models.Article(
        title=article.title,
        description=article.description,
        thumbnailURL=article.thumbnailURL,
        owner_id=userID,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_article(db: Session, article: schemas.ArticleUpdate):
    up_article = (
        db.query(models.Article).filter(models.Article.id == int(article.id)).first()
    )
    up_article.title = article.title
    up_article.description = article.description
    up_article.thumbnailURL = article.thumbnailURL
    # article.updated_at = datetime.now
    db.commit()
    db.refresh(up_article)
    return up_article


def delete_article(db: Session, article: schemas.ArticleDelete):
    db.query(models.Article).filter(models.Article.id == int(article.id)).delete()
    db.commit()
    return


def image_upload(file: UploadFile = File(...)):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=getenv("S3_SECRET_KEY"),
        region_name=getenv("S3_REGION_NAME"),
    )
    upload_filename = os.path.join("article", file.filename)
    try:
        s3.upload_fileobj(
            file.file,
            getenv("S3_BUCKET_NAME"),
            upload_filename,
            ExtraArgs={"ContentType": "image/jpeg", "ACL": "public-read"},
        )
    except boto3.exceptions.S3UploadFailedError:
        print("S3へのアップロードでエラーが発生しました")
        raise boto3.exceptions.S3UploadFailedError
    url = os.path.join(getenv("BUCKET_URL"), upload_filename)
    return url
