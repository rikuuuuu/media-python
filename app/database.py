from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
load_dotenv()

user_name = getenv('DB_USER')
password = getenv('DB_PASSWORD')
host = getenv('DB_HOST')
database_name = getenv('DB_NAME')

SQLALCHEMY_DATABASE_URL = f'mysql://{user_name}:{password}@{host}/{database_name}'

engine = create_engine(
   SQLALCHEMY_DATABASE_URL, 
#    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()