from telegram import Update
from telegram.ext import ContextTypes

from admin_keyboard import (
    admin_keyboard,
    premium_admin_keyboard,
)

from database import (
    total_users,
    get_premium_users,
)


async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ==========================
    # ADMIN HOME
    # ==========================

    if data == "admin_home":

        premium = len(get_premium_users())

        await query.edit_message_text(
            f"""👑 Student Helping Bot

Admin Dashboard

👥 Total Users: {total_users()}
👑 Premium Users: {premium}

━━━━━━━━━━━━━━

Choose an option 👇""",
            reply_markup=admin_keyboard(),
        )

        return


    # ==========================
    # PREMIUM PANEL
    # ==========================

    if data == "admin_premium":

        await query.edit_message_text(
            """⭐ Premium Management

Choose an option below 👇""",
            reply_markup=premium_admin_keyboard(),
        )

        return
    if data == "premium_users":

        users = get_premium_users()

        if not users:
            await query.edit_message_text(
                "👑 No Premium users found.",
                reply_markup=premium_admin_keyboard(),
            )
            return

        keyboard = []

        for row in users:
            keyboard.append([
                InlineKeyboardButton(
                    row["full_name"],
                    callback_data=f"premium_user_{row['user_id']}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="admin_premium"
            )
        ])

        await query.edit_message_text(
            "👑 Premium Users",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return