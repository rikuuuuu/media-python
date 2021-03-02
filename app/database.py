from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# user_name = "root"
# password = "Riku@0369"
# host = "yanorikuunoMacBook-puro.local"
# database_name = "media_fastapi"

user_name = "sumomo"
password = "riku0369"
host = "database-1.cnjzw96avif2.ap-northeast-1.rds.amazonaws.com:3306"
database_name = "media_fastapi"

SQLALCHEMY_DATABASE_URL = f'mysql://{user_name}:{password}@{host}/{database_name}'

engine = create_engine(
   SQLALCHEMY_DATABASE_URL, 
#    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()