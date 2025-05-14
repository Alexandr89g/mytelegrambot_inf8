import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Получаем токен из переменной окружения
TOKEN = os.environ["BOT_TOKEN"]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот-помощник по информатике 8 класса.\n\n"
        "Напиши:\n"
        "👉 'новая тема' — изучим новую тему\n"
        "👉 'повторение' — повторим пройденное\n"
        "👉 'сор' — подготовка к СОР"
    )

# Сообщения: текстовые команды
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "новая тема" in text:
        await update.message.reply_text("📘 Давай изучим новую тему. Например: 'Циклы в Python'.")
    elif "повторение" in text:
        await update.message.reply_text("🔁 Повторим материал! Напиши, что именно повторить.")
    elif "сор" in text:
        await update.message.reply_text("📝 Подготовка к СОР. Укажи тему, и я помогу с заданиями.")
    else:
        await update.message.reply_text("❓ Я тебя не понял. Напиши 'новая тема', 'повторение' или 'сор'.")

# Настройка и запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Бот запущен. Ожидаю сообщения...")
app.run_polling()
