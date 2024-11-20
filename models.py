from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class CEFRLevel(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    username = Column(String)
    current_level = Column(Enum(CEFRLevel), default=CEFRLevel.A1)
    streak_count = Column(Integer, default=0)
    last_active = Column(DateTime)
    
    progress = relationship("Progress", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    level = Column(Enum(CEFRLevel))
    audio_url = Column(String)
    order = Column(Integer)
    
    quiz = relationship("Quiz", back_populates="lesson")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    question = Column(String)
    correct_answer = Column(String)
    options = Column(String)  # JSON string of options
    
    lesson = relationship("Lesson", back_populates="quiz")
    results = relationship("QuizResult", back_populates="quiz")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed = Column(DateTime)
    
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson")

class QuizResult(Base):
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Float)
    completed = Column(DateTime)
    
    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")