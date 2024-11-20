from telegram import Update
from telegram.ext import ContextTypes
from .lesson_handler import handle_lesson_menu, start_lesson

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
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