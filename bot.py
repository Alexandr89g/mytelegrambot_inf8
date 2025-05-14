import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.environ["BOT_TOKEN"]

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я бот-помощник по информатике. Напиши 'новая тема', чтобы начать урок.")

# Создание и запуск приложения
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("✅ Бот запущен. Ожидаю сообщения...")
app.run_polling()

