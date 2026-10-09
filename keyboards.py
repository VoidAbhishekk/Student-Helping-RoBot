from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from files import get_available_years, get_available_shifts, PYQ_FOLDER, ANSWERKEY_FOLDER


def home_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📚 PYQ Papers", callback_data="pyq"),
            InlineKeyboardButton("✅ Answer Keys", callback_data="answerkey"),
        ],
        [InlineKeyboardButton("📢 Latest Updates", callback_data="latest_updates")],
        [InlineKeyboardButton("📝 Request a Paper", callback_data="request_paper")],
        [InlineKeyboardButton("💡 Suggestion", callback_data="suggest")],
        [InlineKeyboardButton("👤 My Profile", callback_data="profile")],
        [InlineKeyboardButton("ℹ️ About Bot", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)


def pyq_year_keyboard():
    keyboard = [
        [InlineKeyboardButton(f"📄 PET {year}", callback_data=f"pyq_{year}")]
        for year in get_available_years(PYQ_FOLDER)
    ]
    if not keyboard:
        keyboard.append([InlineKeyboardButton("No papers available yet", callback_data="home")])
    keyboard.append([InlineKeyboardButton("🏠 Home", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)


def answerkey_year_keyboard():
    keyboard = [
        [InlineKeyboardButton(f"📄 PET {year}", callback_data=f"answer_{year}")]
        for year in get_available_years(ANSWERKEY_FOLDER)
    ]
    if not keyboard:
        keyboard.append([InlineKeyboardButton("No answer keys available yet", callback_data="home")])
    keyboard.append([InlineKeyboardButton("🏠 Home", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)


def pyq_shift_keyboard(year):
    keyboard = [
        [InlineKeyboardButton(f"📄 Shift {shift}", callback_data=f"pyqfile_{year}_{shift}")]
        for shift in get_available_shifts(PYQ_FOLDER, year)
    ]
    if not keyboard:
        keyboard.append([InlineKeyboardButton("No shifts available", callback_data="home")])
    keyboard.extend([
        [InlineKeyboardButton("⬅ Back", callback_data="pyq")],
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ])
    return InlineKeyboardMarkup(keyboard)


def answerkey_shift_keyboard(year):
    keyboard = [
        [InlineKeyboardButton(f"📄 Shift {shift}", callback_data=f"answerfile_{year}_{shift}")]
        for shift in get_available_shifts(ANSWERKEY_FOLDER, year)
    ]
    if not keyboard:
        keyboard.append([InlineKeyboardButton("No shifts available", callback_data="home")])
    keyboard.extend([
        [InlineKeyboardButton("⬅ Back", callback_data="answerkey")],
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ])
    return InlineKeyboardMarkup(keyboard)
