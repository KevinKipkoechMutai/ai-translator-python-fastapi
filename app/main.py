from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from schemas import TranslationRequestSchema
from sqlalchemy.orm import Session
from database import get_db
import models

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", { "request": request })

@app.post("/translate")
async def translate(request: TranslationRequestSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print(request.text)
    print(request.languages)

    # my_dict = request.model_dump()

    request_data = models.TranslationRequest(
        text=request.text,
        languages=request.languages
    )

    db.add(request_data)
    db.commit()
    db.refresh(request_data)

    print("submission completed")


@app.get("/translate/{request_id}")
async def get_translation_status(request_id: int, request: Request, db: Session = Depends(get_db)):
    request_obj = db.query(models.TranslationRequest).filter(models.TranslationRequest.id == request_id).first()
    if not request_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    
    if request_obj.status == "in progress":
        return { "status": request_obj.status }
    
    translations = db.query(models.TranslationResult).filter(models.TranslationResult.request_id == request_id ).all()

    return templates.TemplateResponse("results.html", {"request": request, "translations": translations})
