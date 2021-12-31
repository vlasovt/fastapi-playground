from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False
    }
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_base = declarative_base()

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()
    


