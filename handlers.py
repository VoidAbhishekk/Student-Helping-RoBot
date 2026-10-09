import os
from telegram import Update
from telegram.ext import ContextTypes

from database import add_user, get_user, get_latest_update
from keyboards import (
    home_keyboard, pyq_year_keyboard, answerkey_year_keyboard,
    pyq_shift_keyboard, answerkey_shift_keyboard,
)
from utils import format_message
from files import get_pyq_file, get_answerkey_file

OWNER_ID = int(os.getenv("OWNER_ID", "0"))


def _home_text(first_name: str) -> str:
    return f"""👋 Hello, {first_name}!

Welcome to Student Helping Bot 📚

Your personal assistant for government exam preparation.

Choose an option below 👇"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user)
    await update.effective_message.reply_text(
        format_message(_home_text(user.first_name or "there")),
        reply_markup=home_keyboard(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    user = query.from_user

    if data == "home":
        await query.edit_message_text(
            format_message(_home_text(user.first_name or "there")),
            reply_markup=home_keyboard(),
        )

    elif data == "pyq":
        await query.edit_message_text(
            format_message("📚 Previous Year Question Papers\n\nSelect the exam year."),
            reply_markup=pyq_year_keyboard(),
        )

    elif data == "answerkey":
        await query.edit_message_text(
            format_message("✅ Answer Keys\n\nSelect the exam year."),
            reply_markup=answerkey_year_keyboard(),
        )

    elif data == "latest_updates":
        latest = get_latest_update()
        message = (
            f"📢 Latest Update\n\n{latest}"
            if latest else
            "📢 Latest Updates\n\nThere are no announcements yet. Please check again later!"
        )
        await query.edit_message_text(
            format_message(message), reply_markup=home_keyboard()
        )

    elif data == "request_paper":
        context.user_data["waiting_for_request"] = True
        context.user_data["waiting_for_suggestion"] = False
        await query.message.reply_text(
            format_message(
                "📝 Request a Paper\n\n"
                "Send the exam name, year, and shift you need.\n\n"
                "Example: UPSSSC PET 2024, Shift 2.\n"
                "You can include any other useful details too."
            )
        )

    elif data == "suggest":
        context.user_data["waiting_for_suggestion"] = True
        context.user_data["waiting_for_request"] = False
        await query.message.reply_text(
            format_message(
                "💡 Send your suggestion in your next message.\n\n"
                "For example: request a feature, report an issue, or suggest more papers."
            )
        )

    elif data == "profile":
        add_user(user)
        profile = get_user(user.id) or {}
        username = f"@{user.username}" if user.username else "Not set"
        registered = profile.get("registered_at") or "Not available"
        text = (
            "👤 My Profile\n\n"
            f"🆔 User ID: {user.id}\n"
            f"👤 Name: {user.full_name}\n"
            f"🔗 Username: {username}\n"
            f"📅 Registered: {registered}"
        )
        await query.edit_message_text(
            format_message(text), reply_markup=home_keyboard()
        )

    elif data == "about":
        text = """ℹ️ About Student Helping Bot

Student Helping Bot is built to make government exam preparation resources easier to access.

✨ Features
• Previous Year Question Papers (PYQs)
• Answer Keys
• Latest announcements
• Paper requests
• Suggestions and feedback
• Personal profile

👨‍💻 Developer: Abhishek Singh
🛠️ Built with: Python and Telegram Bot API
📩 Contact: @VoidAbhishekk

This bot was created to help students find study resources more conveniently. Thank you for using it! ❤️"""
        await query.edit_message_text(
            format_message(text), reply_markup=home_keyboard()
        )

    elif data.startswith("pyqfile_"):
        _, year, shift = data.split("_", 2)
        pdf_path = get_pyq_file(year, shift)
        try:
            with open(pdf_path, "rb") as pdf:
                await query.message.reply_document(
                    document=pdf,
                    caption=format_message(
                        f"📄 PET {year}\n\nShift {shift}\n\n✅ PDF sent successfully."
                    ),
                )
        except FileNotFoundError:
            await query.message.reply_text(
                format_message("❌ Sorry, this paper file is not available right now.")
            )

    elif data.startswith("answerfile_"):
        _, year, shift = data.split("_", 2)
        pdf_path = get_answerkey_file(year, shift)
        try:
            with open(pdf_path, "rb") as pdf:
                await query.message.reply_document(
                    document=pdf,
                    caption=format_message(
                        f"✅ PET {year} Answer Key\n\nShift {shift}\n\nPDF sent successfully."
                    ),
                )
        except FileNotFoundError:
            await query.message.reply_text(
                format_message("❌ Sorry, this answer key file is not available right now.")
            )

    elif data.startswith("pyq_"):
        year = data.split("_", 1)[1]
        await query.edit_message_text(
            format_message(
                f"📚 PET Previous Year Papers\n\nSelected Year: {year}\n\nChoose a shift."
            ),
            reply_markup=pyq_shift_keyboard(year),
        )

    elif data.startswith("answer_"):
        year = data.split("_", 1)[1]
        await query.edit_message_text(
            format_message(
                f"✅ PET Answer Keys\n\nSelected Year: {year}\n\nChoose a shift."
            ),
            reply_markup=answerkey_shift_keyboard(year),
        )


async def receive_suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route ordinary text messages to whichever user flow is active."""
    if not update.message or not update.message.text:
        return
    is_request = context.user_data.get("waiting_for_request")
    is_suggestion = context.user_data.get("waiting_for_suggestion")
    if not (is_request or is_suggestion):
        return

    user = update.effective_user
    message = update.message.text.strip()
    username = f"@{user.username}" if user.username else "Not set"

    if is_request:
        context.user_data["waiting_for_request"] = False
        subject = "📝 New Paper Request"
        label = "Request"
        confirmation = "✅ Your paper request has been sent to the developer. Thank you!"
    else:
        context.user_data["waiting_for_suggestion"] = False
        subject = "💡 New Suggestion"
        label = "Suggestion"
        confirmation = "✅ Thank you! Your suggestion has been sent to the developer."

    owner_message = (
        f"{subject}\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: {username}\n\n"
        f"{label}:\n{message}"
    )
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=owner_message)
    except Exception:
        await update.message.reply_text(
            format_message(
                "❌ Sorry, your message could not be delivered right now. Please try again later."
            )
        )
        return
    await update.message.reply_text(format_message(confirmation))
