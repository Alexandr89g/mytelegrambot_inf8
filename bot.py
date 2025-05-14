from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник по информатике. Напиши 'новая тема' чтобы начать.")

app = ApplicationBuilder().token("7718887052:AAEKqkBtoKSmqjguU5H_GNHhuybhw9CUNe4").build()
app.add_handler(CommandHandler("start", start))

print("Бот запущен!")
app.run_polling()
