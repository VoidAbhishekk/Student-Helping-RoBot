from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID
from database import add_user

from keyboards import (
    home_keyboard,
    pyq_year_keyboard,
    answerkey_year_keyboard,
    pyq_shift_keyboard,
    answerkey_shift_keyboard,
)

from utils import format_message

from files import (
    get_pyq_file,
    get_answerkey_file,
)
# -------------------------------
# /start
# -------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(user)
    
    text = f"""
👋 Hello, {user.first_name}!
Username: @{user.username}
User ID: {user.id}

Welcome to Helping RoBot.

I'm your personal helping bot.

Please choose an option below:

📚 PYQs
📝 Answer Keys
💡 Suggestions
"""

    await update.message.reply_text(
        format_message(text),
        reply_markup=home_keyboard()
    )

# -------------------------------
# BUTTON HANDLER
# -------------------------------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "home":

        user = query.from_user.first_name

        text = f"""
👋 Hello, {user}!

Welcome to Helping RoBot.

I'm your personal helping bot.

Please choose an option below:

📚 Previous Year Papers
📝 Answer Keys
💡 Suggestions
"""

        await query.edit_message_text(
            format_message(text),
            reply_markup=home_keyboard()
        )

    elif query.data == "pyq":

        await query.edit_message_text(
            format_message(
                "📚 Previous Year Papers\n\nSelect the exam year."
            ),
            reply_markup=pyq_year_keyboard()
        )

    elif query.data == "answerkey":

        await query.edit_message_text(
            format_message(
                "📝 Answer Keys\n\nSelect the exam year."
            ),
            reply_markup=answerkey_year_keyboard()
        )
# ---------------- PYQ YEAR ----------------

    elif query.data.startswith("pyq_"):

        year = query.data.split("_")[1]

        await query.edit_message_text(
            format_message(
                f"📚 PET Previous Year Papers\n\nSelected Year: {year}\n\nChoose a shift."
            ),
            reply_markup=pyq_shift_keyboard(year)
        )


# ---------------- ANSWER KEY YEAR ----------------

    elif query.data.startswith("answer_"):

        year = query.data.split("_")[1]

        await query.edit_message_text(
            format_message(
                f"📝 PET Answer Keys\n\nSelected Year: {year}\n\nChoose a shift."
            ),
            reply_markup=answerkey_shift_keyboard(year)
        )

# ---------------- ABOUT OWNER ----------------

    elif query.data == "about":

        text = """
👨‍💻 About Owner

Developer: Abhishek Singh
Student of BCA (@ MPGI)

🤖 This bot was developed using Python and the Telegram Bot API.

I made this bot specially for my loving girlfriend 
(@ajadpanchhi)

📩 Contact:
@VoidAbhishekk

Thank you for using this bot! ❤️
"""

        await query.edit_message_text(
            format_message(text),
            reply_markup=home_keyboard()
        )
    elif query.data == "suggest":

        await query.message.reply_text(
            "💡 Send your suggestion below.\n\n"
            "Example:\n"
            "• Add more options\n"
            "• Upload more pyqs\n"
            "• Improve UI\n"
            "Something else 👇👇"
        )
        
        context.user_data["waiting_for_suggestion"] = True

# ---------------- PYQ PDF ----------------

    elif query.data.startswith("pyqfile_"):

        _, year, shift = query.data.split("_")

        pdf_path = get_pyq_file(year, shift)

        await query.message.reply_document(
            document=open(pdf_path, "rb"),
            caption=format_message(
                f"""📄 PET {year}

Shift {shift}

✅ PDF Sent Successfully."""
            )
        )



# ---------------- ANSWER KEY PDF ----------------

    elif query.data.startswith("answerfile_"):

        _, year, shift = query.data.split("_")

        pdf_path = get_answerkey_file(year, shift)

        await query.message.reply_document(
            document=open(pdf_path, "rb"),
            caption=format_message(
                f"""📝 PET {year} Answer Key

Shift {shift}

✅ Answer Key Sent Successfully."""
            )
        )

async def receive_suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("waiting_for_suggestion"):
        return

    context.user_data["waiting_for_suggestion"] = False

    user = update.effective_user

    suggestion = update.message.text

    text = f"""
📩 New Suggestion

👤 Name: {user.first_name}
🆔 ID: {user.id}
📛 Username: @{user.username if user.username else 'None'}

💬 Suggestion:

{suggestion}
"""

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=text
    )

    await update.message.reply_text(
        "✅ Thank you! Your suggestion has been sent to the developer."
    )