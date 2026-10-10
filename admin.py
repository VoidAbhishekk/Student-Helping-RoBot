import os
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from admin_keyboard import admin_keyboard
import random
import string
from database import (
    total_users,
    get_all_users,
    save_latest_update,
    save_premium_key,
    get_premium_users,
    revoke_premium,
)

OWNER_ID = int(os.getenv("OWNER_ID", "0"))


def _is_owner(update: Update) -> bool:
    return bool(update.effective_user and update.effective_user.id == OWNER_ID)

def generate_access_key():
    chars = string.ascii_uppercase + string.digits

    parts = [
        "".join(random.choices(chars, k=4))
        for _ in range(3)
    ]

    return "SHB-" + "-".join(parts)
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied.")
        return

    await update.effective_message.reply_text(
        f"""👑 Student Helping Bot

Admin Dashboard

👥 Total Users: {total_users()}

━━━━━━━━━━━━━━

Choose an option below 👇""",
        reply_markup=admin_keyboard(),
    )


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied. ❌")
        return
    all_users = get_all_users()
    await update.effective_message.reply_text(f"👥 Total registered users: {len(all_users)}")
    if not all_users:
        return
    chunk = ""
    for row in all_users:
        candidate = f"{chunk}\n{row[0]}".strip()
        if len(candidate) > 3500:
            await update.effective_message.reply_text(chunk)
            chunk = str(row[0])
        else:
            chunk = candidate
    if chunk:
        await update.effective_message.reply_text(chunk)


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

async def createkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied.")
        return

    key = generate_access_key()

    save_premium_key(key)

    await update.effective_message.reply_text(
        f"✅ Premium Key Created\n\n<code>{key}</code>",
        parse_mode="HTML",
    )

async def premiumusers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(">>> premiumusers command called")

    if not _is_owner(update):
        await update.effective_message.reply_text("❌ Access denied.")
        return

    users = get_premium_users()

    if not users:
        await update.effective_message.reply_text(
            "👑 There are no Premium users."
        )
        return

    text = "👑 Premium Users\n\n"

    for i, row in enumerate(users, start=1):

        username = f"@{row[2]}" if row[2] else "Not set"

        text += (
            f"{i}. {row[1]}\n"
            f"🆔 {row[0]}\n"
            f"👤 {username}\n"
            f"📅 {row[3]}\n\n"
        )

    text += f"━━━━━━━━━━━━━━\n\nTotal Premium Users: {len(users)}"

    await update.effective_message.reply_text(text)