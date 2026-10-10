from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def admin_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="admin_users",
            ),
            InlineKeyboardButton(
                "⭐ Premium",
                callback_data="admin_premium",
            ),
        ],
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="admin_broadcast",
            ),
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="admin_stats",
            ),
        ],
        [
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="admin_settings",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)