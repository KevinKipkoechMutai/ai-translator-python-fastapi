from sqlalchemy.orm import Session
from fastapi import Depends
from models import TranslationResult, TranslationRequest, IndividualTranslations
from database import get_db
import openai
import os
from dotenv import load_dotenv
from typing import List
import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

async def translate_text(text: str, language: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following text to {language}:"},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

async def process_translations(request_id: int, text: str, languages: List[str], db: Session = Depends(get_db)):
    for language in languages:
        translated_text = await translate_text(text, language)
        translation_result = TranslationResult(
            request_id=request_id, language=language, translated_text=translated_text
        )
        individual_translation=IndividualTranslations(
            request_id=request_id, translated_text=translated_text
        )
        db.add(translation_result)
        db.add(individual_translation)
        db.commit()
    
    request = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
    request.status = "completed"
    request.updated_at = datetime.utcnow()
    db.add(request)
    db.commit()