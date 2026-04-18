import os
from telethon.sessions import StringSession
from telethon import TelegramClient
from config import API_ID, API_HASH, STRING_SESSION, MAX_SIZE

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def send(chat_id, file, bot):
    size = os.path.getsize(file)

    if size <= MAX_SIZE:
        msg = await bot.send_document(chat_id, open(file, "rb"))
        return msg.document.file_id
    else:
        await client.start()
        msg = await client.send_file(chat_id, file)
        return msg.file.id
