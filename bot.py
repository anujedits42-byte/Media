import re, asyncio, shutil, threading, os
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from telegram.constants import ChatAction

from web import app
from config import BOT_TOKEN
from downloader import download
from uploader import send
from ui import main_ui, quality_ui
from cache import get, set
from queue_system import queue, worker
from progress import make_progress_hook
from users import add_user
from admin import stats, broadcast


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


def extract(text):
    m = re.search(r"https?://[^\s]+", text)
    return m.group(0) if m else None


def greeting():
    h = datetime.now().hour
    return "🌅 Morning" if h < 12 else "🌙 Evening"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)

    msg = await update.message.reply_text("🧠")

    steps = ["Loading...", "Preparing...", "Almost ready...", "Done!"]

    for s in steps:
        await asyncio.sleep(0.5)
        await msg.edit_text(s)

    bot = await context.bot.get_me()

    await msg.edit_text(
        f"{greeting()}, {user.first_name}\n\n🎬 Smart Downloader",
        reply_markup=main_ui(bot.username)
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = extract(update.message.text)

    if not url:
        return await update.message.reply_text("Send valid link")

    context.user_data["url"] = url

    cached = get(url)
    if cached:
        return await update.message.reply_document(cached)

   # ✅ NEW: fetch video info (thumbnail + title etc.)
    info = await asyncio.to_thread(download.get_info, url)

    # 📸 Show preview first
    await update.message.reply_photo(
        photo=info["thumbnail"],
        caption=build_caption(info),
        reply_markup=quality_ui(info, url),
        parse_mode="Markdown"
    )
    
    await update.message.reply_text(
        "Select quality",
        reply_markup=quality_ui(url)
    )


async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, url = query.data.split("|")
    msg = await query.message.reply_text("Processing...")

    async def task():
        try:
            hook = make_progress_hook(msg)
            quality = "best" if action == "mp3" else action.replace("q", "")

            files, folder = await asyncio.to_thread(
                download, url, quality, hook
            )

            for f in files:
                fid = await send(query.message.chat_id, f, context.bot)
                set(url, fid)

            await msg.delete()
            shutil.rmtree(folder, ignore_errors=True)

        except Exception as e:
            await msg.edit_text(f"Error: {e}")

    await queue.put(task)


def main():
    threading.Thread(target=run_web).start()

    app_bot = Application.builder().token(BOT_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("stats", stats))
    app_bot.add_handler(CommandHandler("broadcast", broadcast))

    app_bot.add_handler(MessageHandler(filters.TEXT, handle))
    app_bot.add_handler(CallbackQueryHandler(click))

    asyncio.get_event_loop().create_task(worker())

    app_bot.run_polling()


if __name__ == "__main__":
    main()
