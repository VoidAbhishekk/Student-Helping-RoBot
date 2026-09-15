from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from files import (
    get_available_years,
    get_available_shifts,
    PYQ_FOLDER,
    ANSWERKEY_FOLDER
)


# ---------------- HOME ---------------- #

def home_keyboard():

    keyboard = [
        [
            InlineKeyboardButton("📚 PYQs", callback_data="pyq"),
            InlineKeyboardButton("📝 Answer Keys", callback_data="answerkey")
        ],
        [
            InlineKeyboardButton("💡 Suggestions", callback_data="suggest")
        ],
        [
            InlineKeyboardButton("👤 About Owner", callback_data="about")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# ---------------- PYQ YEARS ---------------- #

def pyq_year_keyboard():

    keyboard = []

    years = get_available_years(PYQ_FOLDER)

    for year in years:
        keyboard.append([
            InlineKeyboardButton(
                f"📄 PET {year}",
                callback_data=f"pyq_{year}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🏠 Home", callback_data="home")
    ])

    return InlineKeyboardMarkup(keyboard)


# ---------------- ANSWER KEY YEARS ---------------- #

def answerkey_year_keyboard():

    keyboard = []

    years = get_available_years(ANSWERKEY_FOLDER)

    for year in years:
        keyboard.append([
            InlineKeyboardButton(
                f"📄 PET {year}",
                callback_data=f"answer_{year}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🏠 Home", callback_data="home")
    ])

    return InlineKeyboardMarkup(keyboard)


# ---------------- PYQ SHIFTS ---------------- #

def pyq_shift_keyboard(year):

    keyboard = []

    shifts = get_available_shifts(PYQ_FOLDER, year)
    print(shifts)

    for shift in shifts:

        keyboard.append([
            InlineKeyboardButton(
                f"📄 Shift {shift}",
                callback_data=f"pyqfile_{year}_{shift}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅ Back", callback_data="pyq")
    ])

    keyboard.append([
        InlineKeyboardButton("🏠 Home", callback_data="home")
    ])

    return InlineKeyboardMarkup(keyboard)


# ---------------- ANSWER KEY SHIFTS ---------------- #

def answerkey_shift_keyboard(year):

    keyboard = []

    shifts = get_available_shifts(ANSWERKEY_FOLDER, year)

    for shift in shifts:

        keyboard.append([
            InlineKeyboardButton(
                f"📄 Shift {shift}",
                callback_data=f"answerfile_{year}_{shift}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅ Back", callback_data="answerkey")
    ])

    keyboard.append([
        InlineKeyboardButton("🏠 Home", callback_data="home")
    ])

    return InlineKeyboardMarkup(keyboard)