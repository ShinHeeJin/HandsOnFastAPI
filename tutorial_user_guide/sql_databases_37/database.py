from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import the SQLAlchemy parts

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
"""
By default SQLite will only allow one thread to communicate with it, assuming that each thread would handle an independent request.
This is to prevent accidentally sharing the same connection for different things (for different requests).
But in FastAPI, using normal functions (def) more than one thread could interact with the database for the same request, so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.
Also, we will make sure each request gets its own database connection session in a dependency, so there's no need for that default mechanism.
"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
