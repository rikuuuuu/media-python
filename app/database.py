from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

user_name = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")
database_name = getenv("DB_NAME")
port = getenv("DB_PORT")

SQLALCHEMY_DATABASE_URL = (
    f"mysql://{user_name}:{password}@{host}/{database_name}?charset=utf8"
)

print("SQLALCHEMY_DATABASE_URL: ", SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding="utf-8",
    echo=True
    #    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)
