import os
import json
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Настройки ===

# Загрузка токенов из переменных окружения
BOT_TOKEN = os.environ["BOT_TOKEN"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# Загрузка тем КТП из JSON-файла
with open("ktp_8class.json", "r", encoding="utf-8") as file:
    ktp_topics = json.load(file)

# === Функция генерации объяснения темы через ChatGPT ===

async def get_theory_from_ai(topic):
    prompt = (
        f"Ты — учитель информатики 8 класса. Объясни тему «{topic}» простыми словами, кратко и понятно, "
        f"для школьника. Приведи пример, если нужно. Не упоминай, что ты ИИ."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=400
    )
    return response["choices"][0]["message"]["content"]

# === Обработчики ===

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 Привет! Я бот-помощник по информатике 8 класса.\n\n"
        "📚 Я работаю строго по школьной программе (КТП).\n"
        "Напиши тему урока, например:\n"
        "👉 переменные\n👉 цикл for\n👉 анализ данных\n"
        "или просто номер недели: 17, 21 и т.п."
    )
    await update.message.reply_text(message)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip().lower()
    found = None

    # Поиск по номеру недели
    if user_text.isdigit() and user_text in ktp_topics:
        found = ktp_topics[user_text]

    # Поиск по названию темы
    if not found:
        for topic_id, topic in ktp_topics.items():
            if user_text in topic.lower():
                found = topic
                break

    if found:
        await update.message.reply_text(f"📘 Тема: {found}\n\n⌛ Генерирую объяснение...")
        explanation = await get_theory_from_ai(found)
        await update.message.reply_text(f"📖 Вот объяснение:\n\n{explanation}")
    else:
        await update.message.reply_text(
            "❗Эта тема не входит в школьную программу (КТП).\n"
            "Попробуй написать точнее или укажи номер недели от 1 до 34."
        )

# === Запуск бота ===

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Бот по КТП 8 класса запущен")
app.run_polling()
