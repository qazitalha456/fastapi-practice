from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "postgresql://postgres:0000@localhost:5432/qazi"

try:
    engine = create_engine(database_url)
    sessionlocal = sessionmaker(bind=engine)
    Base = declarative_base()
    print("SQLAlchemy engine connected successfully.")

    def get_db():
        db=sessionlocal()
        try:
            yield db
        finally:
            db.close()
    print("Database session created successfully.")

except Exception as e:
    print("Error creating engine or session:", e)


