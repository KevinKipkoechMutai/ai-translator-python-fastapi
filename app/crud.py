from sqlalchemy.orm import Session
from fastapi import Depends
import models
from .database import get_db

def create_translation_task(text: str, languages: list, db: Session = Depends(get_db)):
    task = models.TranslationTask(text=text, languages=languages)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_translation_task(db: Session, task_id: int):
    return db.query(models.TranslationTask)

def perform_translation():
    return ""