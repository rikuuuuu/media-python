from typing import List
from fastapi import FastAPI
# HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

from app import user_crud, article_crud, schemas, models

models.Base.metadata.create_all(bind=engine)

from logging import debug, getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

app = FastAPI()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


@app.get("/")
def index():
    return "Hello World"

# User Service
@app.post("/user/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.debug("user ", user)
    db_user = user_crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@app.get("/user/get")
def read_user(user: schemas.UserGet, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=int(user.id))
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/user/update")
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    # db_user = user_crud.get_user(db, user_id=int(user.id))
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return user_crud.update_user(db, item=user)

@app.post("/user/delete")
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    # db_user = user_crud.get_user(db, user_id=int(user.id))
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user(db, item=user)
    return


# Article Service
@app.get("/article/get")
def get_article(article: schemas.ArticleGet, db: Session = Depends(get_db)):
    db_article = article_crud.get_article(db, article_id=int(article.id))
    return db_article

@app.get("/article/all", response_model=List[schemas.Article])
def GetArticleAll(db: Session = Depends(get_db)):
    db_article = article_crud.get_articles(db)
    return db_article

@app.post("/article/create")
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return article_crud.create_article(db=db, item=article)

@app.post("/article/update")
def update_article(article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    return article_crud.update_article(db=db, item=article)

@app.post("/article/delete")
def delete_article(article: schemas.ArticleDelete, db: Session = Depends(get_db)):
    return article_crud.delete_article(db=db, item=article)