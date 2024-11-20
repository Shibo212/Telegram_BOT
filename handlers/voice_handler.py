from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal
from lesson_handler import LessonHandler
from speech_recognition import SpeechHandler

speech_handler = SpeechHandler()

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    lesson_handler = LessonHandler(db, speech_handler)
    
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    voice_data = await file.download_as_bytearray()
    
    # Get current lesson context from user state
    current_lesson_id = context.user_data.get('current_lesson_id')
    if not current_lesson_id:
        await update.message.reply_text(
            "Please start a lesson before practicing pronunciation."
        )
        db.close()
        return
    
    evaluation = await lesson_handler.evaluate_speaking(
        update.effective_user.id,
        voice_data,
        current_lesson_id
    )
    
    feedback_message = (
        f"🎯 Pronunciation Score: {evaluation['score']:.2%}\n\n"
        f"💭 What you said: {evaluation['transcription']}\n"
        f"✨ Reference: {evaluation['reference']}\n\n"
        f"📝 Feedback: {evaluation['feedback']}"
    )
    
    await update.message.reply_text(feedback_message)
    db.close()