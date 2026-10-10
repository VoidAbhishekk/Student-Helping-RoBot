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

def premium_admin_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "👥 Premium Users",
                callback_data="premium_users",
            )
        ],
        [
            InlineKeyboardButton(
                "🔑 Generate Key",
                callback_data="generate_key",
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Delete All Keys",
                callback_data="delete_all_keys",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="admin_home",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)