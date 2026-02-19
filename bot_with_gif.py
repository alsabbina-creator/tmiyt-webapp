"""
Telegram-bot with GIF animation
Version 7.0
"""

import logging
import json
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "8497510993:AAGgBEyHfTWQ9u8mzw6rMsd9njVn42dEO-c"
SUPABASE_URL = "https://aphijwalnzqbvmrgayon.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwaGlqd2FsbnpxYnZtcmdheW9uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA2OTY0NzgsImV4cCI6MjA4NjI3MjQ3OH0.HaKxoUe22Vu_MYHRMBElXtF2wHsjmQVoxM0V75hs4sE"
WELCOME_GIF_URL = "https://alsabbina-creator.github.io/tmiyt-webapp/welcome.gif"

HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_user(telegram_id):
    try:
        r = httpx.get(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS, 
                     params={"telegram_id": f"eq.{telegram_id}"}, timeout=10)
        rows = r.json() if r.status_code == 200 else []
        return rows[0] if rows else None
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    
    user = get_user(update.effective_user.id)
    fname = update.effective_user.first_name
    
    # Если уже зарегистрирован
    if user and user.get("profile_completed"):
        kb = [
            [InlineKeyboardButton("🔍 Найти обмены", callback_data="find")],
            [InlineKeyboardButton("👤 Мой профиль", callback_data="profile")],
        ]
        await update.message.reply_text(f"👋 С возвращением, {fname}!", 
                                       reply_markup=InlineKeyboardMarkup(kb))
        return
    
    # Новый пользователь - отправляем GIF
    await update.message.reply_animation(
        animation=WELCOME_GIF_URL,
        caption="✨ Добро пожаловать в мир обмена без денег!"
    )
    
    # Сразу после GIF - выбор языка
    kb = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
         InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")],
    ]
    
    await update.message.reply_text(
        f"👋 Привет, {fname}!\n\n🌍 Выберите язык:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("lang_"):
        lang = query.data[5:]
        await query.edit_message_text(
            f"✅ Язык выбран: {lang.upper()}\n\n"
            f"Теперь начнём регистрацию!\n\n"
            f"(Здесь будет полная регистрация с согласиями)"
        )
    elif query.data == "find":
        await query.edit_message_text("🔍 Ищу совпадения...")
    elif query.data == "profile":
        await query.edit_message_text("👤 Ваш профиль...")

def main():
    logger.info("Starting bot with GIF animation...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Bot is running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
