from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base
from database import engine, Base


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


Base.metadata.create_all(engine)