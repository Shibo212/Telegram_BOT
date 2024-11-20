from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal
from models import User
from datetime import datetime

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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