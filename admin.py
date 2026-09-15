from telegram import Update
from telegram.ext import ContextTypes

from config import OWNER_ID
from database import total_users


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Access Denied ❌")
        return

    text = f"""
Admin Panel 👑

Total Users 👥: {total_users()}

Available Commands:

/users - Total Users
/broadcast - Broadcast Message
"""

    await update.message.reply_text(text)