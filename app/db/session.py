import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Safe password encoding
raw_password = "Sowmya@#1406"
encoded_password = urllib.parse.quote_plus(raw_password)

# Note: We use the encoded password here
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost:3306/finance_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This is the "Dependency" we will use in our routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()