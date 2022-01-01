from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import urllib

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'todos')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'ascold')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'ascold')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))

POSTGRES_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    POSTGRES_DATABASE_URL #, connect_args={
    #    "check_same_thread": False
    # }
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_base = declarative_base()

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()
    


