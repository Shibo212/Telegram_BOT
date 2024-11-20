from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from models import Lesson, Progress, User
from speech_recognition import SpeechHandler
import json

class LessonHandler:
    def __init__(self, db: Session, speech_handler: SpeechHandler):
        self.db = db
        self.speech_handler = speech_handler

    async def get_next_lesson(self, user_id: int) -> Optional[Dict]:
        """Get the next available lesson for the user."""
        user = self.db.query(User).filter(User.telegram_id == str(user_id)).first()
        if not user:
            return None

        # Get the last completed lesson
        last_progress = (
            self.db.query(Progress)
            .filter(Progress.user_id == user.id)
            .order_by(Progress.completed.desc())
            .first()
        )

        # Get the next lesson
        next_lesson = (
            self.db.query(Lesson)
            .filter(Lesson.level == user.current_level)
            .order_by(Lesson.order)
        )

        if last_progress:
            next_lesson = next_lesson.filter(Lesson.order > last_progress.lesson.order)

        next_lesson = next_lesson.first()

        if next_lesson:
            return {
                "id": next_lesson.id,
                "title": next_lesson.title,
                "content": next_lesson.content,
                "level": next_lesson.level.value,
                "audio_url": next_lesson.audio_url,
            }
        return None

    async def complete_lesson(self, user_id: int, lesson_id: int) -> bool:
        """Mark a lesson as completed for the user."""
        user = self.db.query(User).filter(User.telegram_id == str(user_id)).first()
        if not user:
            return False

        progress = Progress(
            user_id=user.id,
            lesson_id=lesson_id,
            completed=datetime.utcnow()
        )
        self.db.add(progress)
        
        try:
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error completing lesson: {e}")
            self.db.rollback()
            return False

    async def get_lesson_audio(self, lesson_id: int) -> Optional[bytes]:
        """Generate or retrieve audio for a lesson."""
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return None

        try:
            return await self.speech_handler.generate_audio(lesson.content)
        except Exception as e:
            print(f"Error generating lesson audio: {e}")
            return None

    async def evaluate_speaking(self, user_id: int, audio_content: bytes, lesson_id: int) -> Dict:
        """Evaluate user's speaking practice for a lesson."""
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return {"score": 0, "feedback": "Lesson not found"}

        try:
            transcription = await self.speech_handler.transcribe_audio(audio_content)
            score = await self.speech_handler.evaluate_pronunciation(lesson.content, transcription)
            
            feedback = "Excellent!" if score > 0.9 else \
                      "Good job!" if score > 0.7 else \
                      "Keep practicing!"
            
            return {
                "score": score,
                "feedback": feedback,
                "transcription": transcription,
                "reference": lesson.content
            }
        except Exception as e:
            print(f"Error evaluating speaking: {e}")
            return {"score": 0, "feedback": "Error processing audio"}