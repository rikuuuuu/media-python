from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.auth import authenticate, create_tokens, get_current_user, get_current_user_with_refresh_token
from typing import List
from fastapi import FastAPI
# HTTPException
from fastapi.params import Depends
from pydantic.schema import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true
from app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

# Article データベース型 → レスポンス型　変換
def ToResArticle(db_article):
    return schemas.Article(
        id=str(db_article.id),
        title=db_article.title,
        description=db_article.description,
        userID=str(db_article.owner_id),
        createdAt=str(db_article.created_at),
        updatedAt=str(db_article.updated_at)
    )

# User データベース型 → レスポンス型　変換
def ToResUser(db_user):
    return schemas.User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        is_active=db_user.is_active
    )


@app.get("/")
def index():
    return 'Hello World!'

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # """トークン発行"""
    user = authenticate(db=db, username=form.username, password=form.password)
    return create_tokens(db=db, user_id=user.id)


@app.get("/refresh_token/")
async def refresh_token(current_user: models.User = Depends(get_current_user_with_refresh_token)):
    # """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)


@app.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    # """ログイン中のユーザーを取得"""
    return current_user

# User Service
@app.post("/user/create")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = user_crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    db_user = user_crud.create_user(db=db, user=user)
    return ToResUser(db_user)

@app.get("/user/get")
def read_user(user: schemas.UserGet, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=int(user.id))
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return ToResUser(db_user)

@app.post("/user/update")
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    # db_user = user_crud.get_user(db, user_id=int(user.id))
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    db_user = user_crud.update_user(db, item=user)
    return ToResUser(db_user)

@app.post("/user/delete")
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    # db_user = user_crud.get_user(db, user_id=int(user.id))
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user(db, item=user)
    return


# Article Service
@app.get("/article/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    # logger.debug("article ", article)
    db_article = article_crud.get_article(db, article_id=article_id)
    return ToResArticle(db_article)

@app.post("/article/all")
def GetArticleAll(db: Session = Depends(get_db)):
    db_articles = article_crud.get_articles(db)
    articleList = []

    for db_article in db_articles:
        article: schemas.Article = ToResArticle(db_article)
        articleList.append(article)

    return articleList

@app.post("/article/create")
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = article_crud.create_article(db=db, item=article)
    return ToResArticle(db_article)

@app.post("/article/update")
def update_article(article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    db_article = article_crud.update_article(db=db, item=article)
    return ToResArticle(db_article)

@app.post("/article/delete")
def delete_article(article: schemas.ArticleDelete, db: Session = Depends(get_db)):
    article_crud.delete_article(db=db, item=article)
    return