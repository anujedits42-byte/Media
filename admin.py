from config import ADMIN_ID
from users import get_users

def is_admin(uid):
    return uid == ADMIN_ID


async def stats(update, context):
    if not is_admin(update.effective_user.id):
        return

    users = get_users()
    await update.message.reply_text(f"👥 Users: {len(users)}")


async def broadcast(update, context):
    if not is_admin(update.effective_user.id):
        return

    msg = " ".join(context.args)
    users = get_users()

    sent = 0

    for uid in users:
        try:
            await context.bot.send_message(uid, msg)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ Sent: {sent}")
