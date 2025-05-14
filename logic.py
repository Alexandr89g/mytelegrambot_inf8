
from calendar import get_school_week
import openai

async def generate_lesson(topic, mode="theory"):
    prompt = f"Ты — учитель информатики. Объясни тему «{topic}» для 8 класса: кратко, понятно, по шагам, с примерами."
    if mode == "practice":
        prompt = f"Составь практические задания по теме «{topic}» для ученика 8 класса по таксономии Блума."
    elif mode == "review":
        prompt = f"Задай 2-3 вопроса на актуализацию знаний по теме «{topic}» для ученика 8 класса."
    elif mode == "test":
        prompt = f"Сделай проверочное задание по теме «{topic}», с автопроверкой и пояснением."

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.6
    )
    return completion["choices"][0]["message"]["content"]
