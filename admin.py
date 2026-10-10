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