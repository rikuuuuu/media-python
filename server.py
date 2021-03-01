from starlette import middleware
from app.main import AdminUserService, ArticleService
from fastapi import FastAPI, Query, Body, Depends, HTTPException
from pydantic import BaseModel, Field
from twirp.asgi import TwirpASGIApp
from twirp.context import Context
# from twirp
# from starlette.applications import Starlette
# from starlette.middleware import Middleware
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
# from starlette.middleware.trustedhost import TrustedHostMiddleware

from sqlalchemy.orm import Session

from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app import models, schemas
from app.database import SessionLocal, engine

from pb import service_article_twirp, entity_article_pb2, entity_admin_user_pb2, service_admin_user_twirp

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

middleware = [
    Middleware(
        CORSMiddleware, 
        allowed_hosts=["*"],
        allow_origins=["*"], 
        allow_methods=["*"], 
        allow_headers=["*"],
        options={}
    ),
    # Middleware(HTTPSRedirectMiddleware)
]

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
#     "*"
# ]

# app.add_middleware(
#     # options={
#     # },
#     CORSMiddleware,
#     allow_origins=["*"],
#     # allow_credentials=True,
#     allow_methods=["POST", "GET"],
#     allow_headers=["Content-Type", "Authorization",],
#     # middleware_class=
# )

# middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     # allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     # middleware_class=
# )

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


articleService = service_article_twirp.ArticleServiceServer(service=ArticleService())
adminUserService = service_admin_user_twirp.AdminUserServiceServer(service=AdminUserService())
app = TwirpASGIApp()
# app._with_middlewares(ctx=Context(), request="", func=middleware)
app.add_service(articleService)
app.add_service(adminUserService)