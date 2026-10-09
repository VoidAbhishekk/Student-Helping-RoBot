import os
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from database import total_users, get_all_users, save_latest_update

OWNER_ID = int(os.getenv("OWNER_ID", "0"))


def _is_owner(update: Update) -> bool:
    return bool(update.effective_user and update.effective_user.id == OWNER_ID)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied.")
        return
    await update.effective_message.reply_text(
        f"👑 Admin Panel\n\n👥 Total Users: {total_users()}\n\n"
        "Available commands:\n"
        "/users — View registered user IDs\n"
        "/broadcast Write your message — Send an announcement to all registered users\n\n"
        "The latest broadcast is saved for the latest Updates button. 📢"
    )


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied. ❌")
        return
    all_users = get_all_users()
    await update.effective_message.reply_text(f"👥 Total registered users: {len(all_users)}")
    # if not all_users:
    #     return
    # chunk = ""
    # for row in all_users:
    #     candidate = f"{chunk}\n{row[0]}".strip()
    #     if len(candidate) > 3500:
    #         await update.effective_message.reply_text(chunk)
    #         chunk = str(row[0])
    #     else:
    #         chunk = candidate
    # if chunk:
    #     await update.effective_message.reply_text(chunk)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied.")
        return
    if not context.args:
        await update.effective_message.reply_text(
            "Usage:\n/broadcast Your announcement here"
        )
        return

    message = " ".join(context.args).strip()
    if not message:
        await update.effective_message.reply_text(
            "Usage:\n/broadcast Your announcement here"
        )
        return

    save_latest_update(message)
    user_ids = get_all_users()
    sent = failed = 0
    for row in user_ids:
        try:
            await context.bot.send_message(
                chat_id=row[0], text=f"📢 Latest Update\n\n{message}"
            )
            sent += 1
        except TelegramError:
            failed += 1

    await update.effective_message.reply_text(
        f"✅ Broadcast finished!\n\nSent: {sent}\nFailed: {failed}\n\n"
        "The announcement is now available in the Latest Updates button."
    )
