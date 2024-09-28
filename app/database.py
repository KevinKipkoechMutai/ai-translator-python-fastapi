from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://aitranslatordb_owner:M09lAbirLKYW@ep-flat-waterfall-a5m8t0n9.us-east-2.aws.neon.tech/aitranslatordb?sslmode=require")

SessionLocal = sessionmaker(autocommit=False, autoflush=False,  bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()