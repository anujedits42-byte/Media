import shutil
import re
import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from telegram.constants import ChatAction

from config import BOT_TOKEN
from downloader import download
from uploader import send
from ui import main_ui, quality_ui
from cache import get, set
from queue_system import queue, worker
from progress import make_progress_hook


def extract(text):
    m = re.search(r"https?://[^\s]+", text)
    return m.group(0) if m else None


def greeting():
    h = datetime.now().hour
    if h < 12:
        return "🌅 Good Morning"
    elif h < 18:
        return "☀️ Good Afternoon"
    return "🌙 Good Evening"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user else "User"
    bot = await context.bot.get_me()

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    msg = await update.message.reply_text("🧠")

    steps = [
        f"👋 Detecting {name}",
        "📡 Analyzing...",
        "⚡ Loading engine...",
        "🎬 Preparing UI...",
        "✅ Ready"
    ]

    for s in steps:
        await asyncio.sleep(0.7)
        try:
            await msg.edit_text(s)
        except:
            pass

    text = (
        f"{greeting()}, *{name}*\n\n"
        "🎬 *Smart Downloader*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🌐 YouTube / Instagram / TikTok\n"
        "🌐 Facebook / Threads\n"
        "🎵 Music MP3\n\n"
        "⚡ Fast • Smart • 2GB+\n\n"
        "👇 Choose option"
    )

    await msg.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_ui(bot.username)
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = extract(update.message.text)

    if not url:
        return await update.message.reply_text("❌ Invalid link")

    context.user_data["url"] = url

    cached = get(url)
    if cached:
        return await update.message.reply_document(cached)

    await update.message.reply_text(
        "🎬 Select quality:",
        reply_markup=quality_ui(url)
    )


async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, url = query.data.split("|")

    msg = await query.message.reply_text("⏳ Starting...")

    async def task():
        try:
            hook = make_progress_hook(msg)

            quality = "best" if action == "mp3" else action.replace("q", "")

            files, folder = await asyncio.to_thread(
                download,
                url,
                quality,
                hook
            )

            for f in files:
                fid = await send(query.message.chat_id, f, context.bot)
                set(url, fid)

            await msg.delete()
            shutil.rmtree(folder, ignore_errors=True)

        except Exception as e:
            await msg.edit_text(f"❌ {e}")

    await queue.put(task)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))
    app.add_handler(CallbackQueryHandler(click))

    asyncio.get_event_loop().create_task(worker())

    app.run_polling()


if __name__ == "__main__":
    main()
