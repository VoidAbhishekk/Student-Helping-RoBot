import os
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters,
)
from handlers import start, button_handler, receive_suggestion
from admin import (
    admin,
    users,
    broadcast,
    createkey,
    premiumusers,
)
from admin_callbacks import admin_callback_handler

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TOKEN environment variable.")
if not os.getenv("OWNER_ID"):
    raise RuntimeError("Missing OWNER_ID environment variable.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("createkey", createkey))
app.add_handler(CommandHandler("ptest", premiumusers))
app.add_handler(
    CallbackQueryHandler(
        admin_callback_handler,
        pattern="^admin_|^premium_|^generate_|^delete_|^user_",
    )
)

app.add_handler(
    CallbackQueryHandler(button_handler)
)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_suggestion))

print("✅ Student Helping Bot Started!")
app.run_polling()