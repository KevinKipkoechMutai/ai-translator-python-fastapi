from sqlalchemy.orm import Session
import models

def create_translation_task(db: Session, text: str, languages: list):
    return ""