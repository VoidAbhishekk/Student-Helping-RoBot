from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from handlers import (
    start,
    button_handler,
    receive_suggestion,
)
from admin import admin


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        receive_suggestion,
    )
)
app.add_handler(CommandHandler("admin", admin))
print("✅ Government Exam Helper Bot Started!")

app.run_polling()