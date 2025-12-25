"""
Telegram Language Pronunciation Bot
Supports English and Korean word/phrase pronunciation
Designed for Render deployment
"""

import os
import logging
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from gtts import gTTS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user language preferences (in production, use a database)
user_languages = {}

# Keyboard for main menu
def get_main_keyboard():
    """Get main menu keyboard"""
    keyboard = [[
        KeyboardButton("🔄 Tilni o'zgartirish")
    ]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_initial_keyboard():
    """Get initial keyboard before language selection"""
    keyboard = [[
        KeyboardButton("🗣️ Tilni tanlash")
    ]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_language_keyboard():
    """Get language selection keyboard"""
    keyboard = [[
        KeyboardButton("🇺🇸 Inglizcha"),
        KeyboardButton("🇰🇷 Koreys")
    ]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

class LanguageBot:
    """Main bot class for handling language pronunciation"""
    
    LANGUAGES = {
        'en': {'name': 'Ingliz', 'code': 'en'},
        'ko': {'name': 'Koreys', 'code': 'ko'}
    }
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user_languages[user_id] = 'en'  # Default to English
        
        welcome_msg = (
            "👋 Til Talaffuzi Botiga xush kelibsiz!\n\n"
            "🎯 Menga ingliz yoki koreys tilida istalgan so'z yoki iboralarni yuboring, "
            "men esa talaffuz audio yuboraman.\n\n"
            "Buyruqlar:\n"
            "/start - Botni boshlash\n"
            "/language - Tilni tanlash\n"
            "/help - Yordam ko'rsatish\n\n"
            f"Joriy til: {LanguageBot.LANGUAGES['en']['name']} 🇺🇸"
        )
        
        await update.message.reply_text(welcome_msg, reply_markup=get_initial_keyboard())
        logger.info(f"User {user_id} started the bot")
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_msg = (
            "📖 Bu botdan qanday foydalanish kerak:\n\n"
            "1️⃣ Tugmalarni bosing yoki /language buyruqdan foydalaning\n"
            "2️⃣ Istalgan so'z yoki iboralarni yuboring\n"
            "3️⃣ Darhol talaffuz audio qabul qiling!\n\n"
            "Misollari:\n"
            "• 'Hello' → Ingliz tilida 'Hello' talaffuzi\n"
            "• '안녕하세요' → Koreys tilida '안녕하세요' talaffuzi\n\n"
            "Istalgan vaqtda tilni o'zgartirishingiz mumkin! 🔄"
        )
        
        await update.message.reply_text(help_msg, reply_markup=get_main_keyboard())
    
    @staticmethod
    async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command"""
        user_id = update.effective_user.id
        current_lang = user_languages.get(user_id, 'en')
        current_lang_name = LanguageBot.LANGUAGES[current_lang]['name']
        
        msg = f"Joriy til: {current_lang_name}\n\nTilni tanlang:"
        
        await update.message.reply_text(msg, reply_markup=get_language_keyboard())
    
    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle keyboard button presses"""
        user_id = update.effective_user.id
        text = update.message.text.strip()
        
        if text == "🗣️ Tilni tanlash":
            current_lang = user_languages.get(user_id, 'en')
            current_lang_name = LanguageBot.LANGUAGES[current_lang]['name']
            msg = f"Joriy til: {current_lang_name}\n\nTilni tanlang:"
            await update.message.reply_text(msg, reply_markup=get_language_keyboard())
        
        elif text == "🔄 Tilni o'zgartirish":
            current_lang = user_languages.get(user_id, 'en')
            current_lang_name = LanguageBot.LANGUAGES[current_lang]['name']
            msg = f"Joriy til: {current_lang_name}\n\nTilni tanlang:"
            await update.message.reply_text(msg, reply_markup=get_language_keyboard())
        
        elif text == "🇺🇸 Inglizcha":
            user_languages[user_id] = 'en'
            await update.message.reply_text(
                "✅ Til Ingliz 🇺🇸 ga o'zgartirildi\n\n"
                "Talaffuzini eshitish uchun so'z yoki iboralarni yuboring!",
                reply_markup=get_main_keyboard()
            )
            logger.info(f"User {user_id} changed language to English")
        
        elif text == "🇰🇷 Koreys":
            user_languages[user_id] = 'ko'
            await update.message.reply_text(
                "✅ Til Koreys 🇰🇷 ga o'zgartirildi\n\n"
                "Talaffuzini eshitish uchun so'z yoki iboralarni yuboring!",
                reply_markup=get_main_keyboard()
            )
            logger.info(f"User {user_id} changed language to Korean")
    
    @staticmethod
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages and generate audio"""
        user_id = update.effective_user.id
        text = update.message.text.strip()
        
        # Check if it's a button press
        if text in ["🗣️ Tilni tanlash", "🔄 Tilni o'zgartirish", "🇺🇸 Inglizcha", "🇰🇷 Koreys"]:
            await LanguageBot.button_callback(update, context)
            return
        
        if not text:
            await update.message.reply_text("Iltimos, so'z yoki iboralarni yuboring!")
            return
        
        # Limit text length
        if len(text) > 500:
            await update.message.reply_text(
                "❌ Matn juda uzun! Maksimal 500 belgi ruxsat etilgan."
            )
            return
        
        # Get user's language preference
        lang_code = user_languages.get(user_id, 'en')
        lang_name = LanguageBot.LANGUAGES[lang_code]['name']
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"🎵 {lang_name} talaffuzi yaratilmoqda..."
        )
        
        try:
            # Generate audio using gTTS
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to BytesIO object
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            audio_file.name = f"{text[:30]}.mp3"
            
            # Delete processing message
            await processing_msg.delete()
            
            # Send audio file
            flag = "🇺🇸" if lang_code == 'en' else "🇰🇷"
            caption = f"{flag} {lang_name}: \"{text}\""
            
            await update.message.reply_audio(
                audio=audio_file,
                caption=caption,
                title=text[:50]
            )
            
            logger.info(f"Audio sent for user {user_id}: {text} ({lang_code})")
            
        except Exception as e:
            logger.error(f"Error generating audio: {e}", exc_info=True)
            await processing_msg.edit_text(
                "❌ Kechirasiz, audiodni yarata olmadim. "
                "Iltimos, boshqa so'z yoki iboralar bilan qayta urinib ko'ring."
            )
    
    @staticmethod
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
            )

def main():
    """Main function to run the bot"""
    # Get bot token from environment variable
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN not found in environment variables.\n"
            "Please set it in Render environment settings."
        )
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", LanguageBot.start))
    application.add_handler(CommandHandler("help", LanguageBot.help_command))
    application.add_handler(CommandHandler("language", LanguageBot.language_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, LanguageBot.handle_text)
    )
    application.add_error_handler(LanguageBot.error_handler)
    
    # Start the bot
    logger.info("🚀 Bot started on Render!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()