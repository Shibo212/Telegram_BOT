from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Lesson, Quiz, User, Progress, QuizResult
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LessonCreate(BaseModel):
    title: str
    content: str
    level: str
    order: int
    audio_url: str = None

class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    level: str
    order: int
    audio_url: str = None

    class Config:
        from_attributes = True

@app.get("/api/lessons", response_model=List[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).order_by(Lesson.order).all()

@app.post("/api/lessons", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_lessons = db.query(Lesson).count()
    total_quizzes = db.query(Quiz).count()
    active_users = db.query(User).filter(
        User.last_active > datetime.utcnow().date()
    ).count()
    
    return {
        "total_users": total_users,
        "total_lessons": total_lessons,
        "total_quizzes": total_quizzes,
        "active_users": active_users
    }