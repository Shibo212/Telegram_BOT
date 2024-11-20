import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from database import SessionLocal
from models import User, Lesson, Quiz, Progress
from datetime import datetime
from speech_recognition import SpeechHandler
from lesson_handler import LessonHandler
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

speech_handler = SpeechHandler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    user = update.effective_user
    
    db_user = db.query(User).filter(User.telegram_id == str(user.id)).first()
    if not db_user:
        db_user = User(
            telegram_id=str(user.id),
            username=user.username,
            last_active=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
    
    keyboard = [
        [
            InlineKeyboardButton("Start Learning 📚", callback_data="menu_lessons"),
            InlineKeyboardButton("My Progress 📊", callback_data="menu_progress")
        ],
        [
            InlineKeyboardButton("Practice Speaking 🗣", callback_data="menu_speaking"),
            InlineKeyboardButton("Take Quiz 📝", callback_data="menu_quiz")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "مرحباً بك في روبوت تعلم اللغة الهولندية! 🇳🇱\n\n"
        "Welcome to the Dutch Learning Bot!\n"
        "I'll help you learn Dutch from Arabic. Choose an option:",
        reply_markup=reply_markup
    )
    db.close()

async def handle_lesson_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    db = SessionLocal()
    lesson_handler = LessonHandler(db, speech_handler)
    
    next_lesson = await lesson_handler.get_next_lesson(update.effective_user.id)
    
    if next_lesson:
        keyboard = [
            [InlineKeyboardButton("Start Lesson", callback_data=f"lesson_{next_lesson['id']}")],
            [InlineKeyboardButton("Back to Menu", callback_data="menu_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📚 Next Lesson: {next_lesson['title']}\n"
            f"Level: {next_lesson['level']}\n\n"
            "Ready to start?",
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(
            "You've completed all available lessons! 🎉\n"
            "Check back later for new content.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back to Menu", callback_data="menu_main")
            ]])
        )
    db.close()

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

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_lessons":
        await handle_lesson_menu(update, context)
    elif query.data == "menu_speaking":
        context.user_data['mode'] = 'speaking_practice'
        await query.edit_message_text(
            "🗣 Speaking Practice Mode\n\n"
            "Send me a voice message to practice your pronunciation."
        )
    elif query.data.startswith("lesson_"):
        lesson_id = int(query.data.split("_")[1])
        context.user_data['current_lesson_id'] = lesson_id
        await start_lesson(update, context, lesson_id)

async def start_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: int):
    db = SessionLocal()
    lesson_handler = LessonHandler(db, speech_handler)
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        await update.callback_query.edit_message_text("Lesson not found.")
        db.close()
        return
    
    # Generate audio for the lesson
    audio_data = await lesson_handler.get_lesson_audio(lesson_id)
    if audio_data:
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=audio_data,
            caption="Listen to the pronunciation 🔊"
        )
    
    keyboard = [
        [
            InlineKeyboardButton("Practice Speaking 🗣", callback_data=f"practice_{lesson_id}"),
            InlineKeyboardButton("Next Lesson ➡️", callback_data="next_lesson")
        ],
        [InlineKeyboardButton("Back to Menu", callback_data="menu_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        f"📚 Lesson: {lesson.title}\n\n"
        f"{lesson.content}\n\n"
        "Listen to the audio and practice your pronunciation!",
        reply_markup=reply_markup
    )
    db.close()

def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.VOICE & ~filters.COMMAND, handle_voice_message))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()