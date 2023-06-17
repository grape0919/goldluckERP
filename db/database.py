from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

from config import database_credential

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{database_credential['user']}:{quote_plus(database_credential['password'])}@{database_credential['host']}:{database_credential['port']}/{database_credential['database']}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgreserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=300,
    pool_size=50
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
