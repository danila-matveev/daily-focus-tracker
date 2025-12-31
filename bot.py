"""
Telegram-бот "Фокус 2026" с напоминаниями и Mini App
"""

import os
import asyncio
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# URL твоего Mini App (после деплоя на Vercel/Netlify)
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-miniapp.vercel.app")

# Твой Telegram ID для напоминаний (узнать: @userinfobot)
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# Время напоминаний (UTC! Бали = UTC+8, значит 6:00 Бали = 22:00 UTC предыдущего дня)
MORNING_TIME = time(hour=22, minute=0)  # 6:00 по Бали
EVENING_TIME = time(hour=13, minute=0)  # 21:00 по Бали


# ===== ТЕКСТЫ =====
CREDO_SHORT = "Делай важное в бизнесе. Внедряй AI. Будь с семьёй. Тренируйся. Остальному — нет."

CREDO_FULL = """🎯 *КРЕДО 2026*

Нет шорткатов. Делай работу. Двигай бизнес каждый день. Внедряй AI — это твоё оружие. Нанимай людей сильнее себя. Считай цифры.

Будь с женой. Будь с дочкой. Без телефона. Полностью. Работа — в кабинете. Семья — в моменте.

Тренируйся. Спи. Ешь белок. Не пей. Не кури. Медитируй. Выбирай позитив, даже когда всё идёт по пизде.

*Шесть опор. Остальному — нет. Проживи этот день как целую жизнь.*"""

MORNING_MESSAGE = """☀️ *Доброе утро!*

{credo}

━━━━━━━━━━━━━━━
*3 ПРИНЦИПА:*
1️⃣ Фокус только на 6 сферах
2️⃣ Моё «да» дорого
3️⃣ Управляю состоянием
━━━━━━━━━━━━━━━

Сегодняшний фокус:
👨‍👩‍👧 Семья — присутствие
🚀 Бизнес — двигай вперёд
🤖 AI — учись и внедряй
📢 Бренд — пробей брешь молчания
💰 Капитал — как гигиена
💪 Здоровье — тренируйся"""

EVENING_MESSAGE = """🌙 *Вечер. Время подвести итоги.*

Открой трекер и отметь:
• Что сделал по каждой сфере
• Победы дня
• Что крало фокус

_Проживи этот день как целую жизнь._"""


# ===== КЛАВИАТУРЫ =====
def get_main_keyboard():
    """Основная клавиатура с Mini App"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📊 Открыть трекер",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton("☀️ Утро", callback_data="morning"),
            InlineKeyboardButton("🌙 Вечер", callback_data="evening"),
        ],
        [InlineKeyboardButton("📜 Полное кредо", callback_data="credo")]
    ])


def get_back_keyboard():
    """Кнопка назад"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("« Назад", callback_data="back")]
    ])


# ===== ОБРАБОТЧИКИ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        f"👋 *Привет!*\n\n"
        f"Это твой трекер фокуса на 2026 год.\n\n"
        f"_{CREDO_SHORT}_\n\n"
        f"Жми кнопку ниже, чтобы открыть трекер 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "morning":
        await query.edit_message_text(
            MORNING_MESSAGE.format(credo=CREDO_SHORT),
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif query.data == "evening":
        await query.edit_message_text(
            EVENING_MESSAGE,
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    
    elif query.data == "credo":
        await query.edit_message_text(
            CREDO_FULL,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif query.data == "back":
        await query.edit_message_text(
            f"_{CREDO_SHORT}_\n\n"
            f"Жми кнопку ниже, чтобы открыть трекер 👇",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )


async def morning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /morning"""
    await update.message.reply_text(
        MORNING_MESSAGE.format(credo=CREDO_SHORT),
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


async def evening_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /evening"""
    await update.message.reply_text(
        EVENING_MESSAGE,
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


# ===== НАПОМИНАНИЯ =====
async def send_morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Утреннее напоминание"""
    if OWNER_ID:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=MORNING_MESSAGE.format(credo=CREDO_SHORT),
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )


async def send_evening_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Вечернее напоминание"""
    if OWNER_ID:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=EVENING_MESSAGE,
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )


# ===== ЗАПУСК =====
def main():
    """Запуск бота"""
    print("🚀 Запуск бота...")
    
    # Создаём приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("morning", morning_command))
    app.add_handler(CommandHandler("evening", evening_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Добавляем напоминания (job queue)
    if OWNER_ID:
        job_queue = app.job_queue
        job_queue.run_daily(send_morning_reminder, time=MORNING_TIME, name="morning")
        job_queue.run_daily(send_evening_reminder, time=EVENING_TIME, name="evening")
        print(f"⏰ Напоминания настроены для ID: {OWNER_ID}")
    else:
        print("⚠️ OWNER_ID не задан — напоминания отключены")
    
    # Запускаем
    print("✅ Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
