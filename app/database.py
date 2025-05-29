from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
sqlite_database_url = "postgresql://postgres:5432@localhost:5432/Fastapi project"
engine = create_engine(sqlite_database_url)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Database connection
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()