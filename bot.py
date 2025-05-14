
import os, json
import openai
from datetime import date
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from calendar import get_school_week
from logic import generate_lesson

openai.api_key = os.environ["OPENAI_API_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

with open("ktp_8class.json", encoding="utf-8") as f:
    topics = json.load(f)

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    user_state[update.effective_user.id] = "menu"
    keyboard = [["📘 Новая тема", "🔁 Повторение"], ["📝 Подготовка к СОР"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, {name}! Я твой помощник по информатике 8 класса.
"
        "Хочешь изучить новую тему, повторить или подготовиться к СОР?",
        reply_markup=reply_markup
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    user_id = update.effective_user.id

    if text == "📘 новая тема":
        week = get_school_week()
        topic = topics.get(str(week), "Тема не найдена")
        await update.message.reply_text(f"Тема недели №{week}: {topic}")
        review = await generate_lesson(topic, "review")
        theory = await generate_lesson(topic, "theory")
        practice = await generate_lesson(topic, "practice")
        test = await generate_lesson(topic, "test")

        await update.message.reply_text(f"🔍 Актуализация:
{review}")
        await update.message.reply_text(f"📖 Теория:
{theory}")
        await update.message.reply_text(f"🛠 Практика:
{practice}")
        await update.message.reply_text(f"✅ Проверка:
{test}")
        await update.message.reply_text("🔚 Оцени себя от 0 до 8 и ответь: Что было понятно, а что — сложно?")
        return

    elif text == "🔁 повторение":
        week = get_school_week()
        done_topics = [f"{n}. {t}" for n, t in topics.items() if int(n) < week]
        await update.message.reply_text("Пройденные темы:
" + "
".join(done_topics))
        return

    elif text == "📝 подготовка к сор":
        week = get_school_week()
        sor_topics = [f"{n}. {t}" for n, t in topics.items() if "СОР" in t and int(n) <= week]
        if sor_topics:
            await update.message.reply_text("Темы для СОР:
" + "
".join(sor_topics))
        else:
            await update.message.reply_text("СОР пока не предвидится 😉")
        return

    await update.message.reply_text("Пожалуйста, выбери один из вариантов: 📘 Новая тема, 🔁 Повторение, 📝 Подготовка к СОР.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.run_polling()
