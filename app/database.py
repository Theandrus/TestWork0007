import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    f"postgresql://{os.getenv('db_user')}:{os.getenv('db_password')}"
    f"@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

