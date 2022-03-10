# import graphene
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from starlette.graphql import GraphQLApp

from app import article_crud, models, schemas, user_crud
from app.auth import (
    authenticate,
    create_tokens,
    get_current_user,
    get_current_user_with_refresh_token,
)
from app.database import SessionLocal, engine
from app.graph_schemas import Mutation, Query

models.Base.metadata.create_all(bind=engine)

from logging import DEBUG, StreamHandler, getLogger

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
        thumbnailURL=db_article.thumbnailURL,
        userID=str(db_article.owner_id),
        createdAt=str(db_article.created_at),
        updatedAt=str(db_article.updated_at),
    )


# User データベース型 → レスポンス型　変換
def ToResUser(db_user):
    return schemas.User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        is_active=db_user.is_active,
    )


# class Query(graphene.ObjectType):
#     hello = graphene.String(name=graphene.String(default_value="stranger"))

#     def resolve_hello(self, info, name):
#         return "Hello " + name

# app.add_route(
#     "/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation))
# )


@app.get("/")
def ping():
    return {"ping": "pong"}


# User Service
@app.get("/user/getme")
async def get_userme(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.post("/token")
async def user_login(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate(db=db, username=form.username, password=form.password)
    return create_tokens(db=db, user_id=user.id)


@app.get("/refresh_token")
async def user_refresh_token(
    current_user: models.User = Depends(get_current_user_with_refresh_token),
):
    return create_tokens(current_user.id)


@app.post("/user/create")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password is too short")
    db_user = user_crud.create_user(db=db, user=user)
    return ToResUser(db_user)


@app.post("/user/update")
def update_user(
    user: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_user = user_crud.get_user(db, user_id=int(current_user.id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = user_crud.update_user(db, user=user, user_id=current_user.id)
    return ToResUser(db_user)


@app.post("/user/delete")
def delete_user(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    db_user = user_crud.get_user(db, user_id=int(current_user.id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user(db, user=current_user)
    return


# Article Service
@app.get("/article/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    # logger.debug("article ", article)
    db_article = article_crud.get_article(db, article_id=article_id)
    return ToResArticle(db_article)


@app.post("/article/all")
def get_article_all(db: Session = Depends(get_db)):
    db_articles = article_crud.get_articles(db)
    articleList = []

    for db_article in db_articles:
        article: schemas.Article = ToResArticle(db_article)
        articleList.append(article)

    return articleList


@app.post("/article/create")
def create_article(
    article: schemas.ArticleCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_article = article_crud.create_article(
        db=db, article=article, userID=int(current_user.id)
    )
    return ToResArticle(db_article)


@app.post("/article/update")
def update_article(
    article: schemas.ArticleUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_article = article_crud.update_article(db=db, article=article)
    return ToResArticle(db_article)


@app.post("/article/delete")
def delete_article(
    article: schemas.ArticleDelete,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    article_crud.delete_article(db=db, article=article)
    return


# Image Upload to S3
@app.post("/image/upload")
def image_upload(
    file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)
):
    url = article_crud.image_upload(file=file)
    return url
