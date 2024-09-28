from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .database import engine, Base


class TranslationRequest(Base):
    __tablename__ = "translation_requests"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    languages = Column(String, nullable=False)
    status = Column(String, default="in progress", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TranslationResult(Base):
    __tablename__ = "translation_results"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_requests.id"), nullable=False)
    language = Column(String, nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class IndividualTranslations(Base):
    __tablename__ = "individual_translations"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_requests.id"), nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# to ensure tables are created in the database
# engine = create_engine("postgresql://aitranslatordb_owner:M09lAbirLKYW@ep-flat-waterfall-a5m8t0n9.us-east-2.aws.neon.tech/aitranslatordb?sslmode=require")
Base.metadata.create_all(engine)