from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal
from models import Lesson, User
from lesson_handler import LessonHandler
from speech_recognition import SpeechHandler

speech_handler = SpeechHandler()

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