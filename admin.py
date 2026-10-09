from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import os

OWNER_ID = int(os.getenv("OWNER_ID"))

from database import total_users, get_all_users


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Access Denied")
        return

    text = f"""
👑 Admin Panel

👥 Total Users: {total_users()}

Available Commands

/users
/broadcast <message>
"""

    await update.message.reply_text(text)


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    users = get_all_users()

    if not users:
        await update.message.reply_text("No users found.")
        return

    text = f"👥 Total Users: {len(users)}\n\n"

    for user in users:
        text += f"{user[0]}\n"

    await update.message.reply_text(text)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/broadcast Your message"
        )
        return

    message = " ".join(context.args)

    users = get_all_users()

    success = 0
    failed = 0

    for user in users:

        try:

            await context.bot.send_message(
                chat_id=user[0],
                text=message
            )

            success += 1

        except:

            failed += 1

    await update.message.reply_text(

        f"""✅ Broadcast Finished

Sent : {success}

Failed : {failed}
"""
    )