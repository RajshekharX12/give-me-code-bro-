import random
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, ContextTypes

# Admin Telegram ID
ADMIN_ID = 5770074932  # Replace with your Telegram ID

# Inline text store (key-value pairs)
INLINE_TEXTS = {
    "example": "This is an example text."
}

# Superior greetings for the admin
GREETINGS = [
    "Hello, sir! Welcome back to the system.",
    "Greetings, sir! All systems are operational.",
    "Welcome, sir. How may I assist you today?",
    "Good to see you, sir. I'm at your service.",
    "Hello, sir. Ready to execute your commands.",
]


async def start(update, context):
    """Start command with admin greeting and list of commands."""
    if update.effective_user.id == ADMIN_ID:
        greeting = random.choice(GREETINGS)
        await update.message.reply_text(
            f"{greeting}\n\nHere are the available commands:\n"
            "/add_text <key>|<text> - Add a new inline text.\n"
            "/remove_text <key> - Remove an existing inline text.\n"
            "/list_texts - List all available inline texts."
        )
    else:
        await update.message.reply_text("Unauthorized access!")


async def inline_query(update, context):
    """Handle inline queries for both links and text."""
    query = update.inline_query.query.strip()

    if query in INLINE_TEXTS:
        # Inline query for text
        result = InlineQueryResultArticle(
            id=query,
            title=f"Send: {query}",
            input_message_content=InputTextMessageContent(INLINE_TEXTS[query])
        )
        await update.inline_query.answer([result], cache_time=0)
    elif query.isdigit():  # If the query is a number, generate a link
        normalized_number = query.zfill(9)  # Ensure the number is 9 digits long
        link = f"https://fragment.com/number/{normalized_number}/code"
        result = InlineQueryResultArticle(
            id=normalized_number,
            title=f"Generate link for {normalized_number}",
            input_message_content=InputTextMessageContent(link)
        )
        await update.inline_query.answer([result], cache_time=0)
    else:
        # Return an empty response if no match
        await update.inline_query.answer([], cache_time=0)


async def add_text(update, context):
    """Admin command to add a new inline text."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized access!")
        return

    if not context.args or "|" not in context.args[0]:
        await update.message.reply_text("Provide text in the format: `<key>|<text>`.")
        return

    # Split the input into key and text
    key, text = context.args[0].split("|", 1)
    INLINE_TEXTS[key.strip()] = text.strip()
    await update.message.reply_text(f"✅ Added inline text for key '{key.strip()}'.")


async def remove_text(update, context):
    """Admin command to remove an inline text."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized access!")
        return

    if not context.args:
        await update.message.reply_text("Provide the key to remove.")
        return

    key = context.args[0].strip()
    if key in INLINE_TEXTS:
        del INLINE_TEXTS[key]
        await update.message.reply_text(f"✅ Removed inline text for key '{key}'.")
    else:
        await update.message.reply_text(f"❌ Key '{key}' not found.")


async def list_texts(update, context):
    """List all current inline texts."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized access!")
        return

    if not INLINE_TEXTS:
        await update.message.reply_text("No inline texts available.")
        return

    text_list = "\n".join([f"{key}: {text}" for key, text in INLINE_TEXTS.items()])
    await update.message.reply_text(f"📜 *Current Inline Texts:*\n{text_list}", parse_mode="Markdown")


def setup_handlers(app):
    """Set up all bot handlers."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_text", add_text))
    app.add_handler(CommandHandler("remove_text", remove_text))
    app.add_handler(CommandHandler("list_texts", list_texts))
    app.add_handler(InlineQueryHandler(inline_query))


if __name__ == "__main__":
    # Replace with your bot token
    bot_token = "YOUR_BOT_TOKEN"
    application = ApplicationBuilder().token(bot_token).build()

    setup_handlers(application)
    application.run_polling()
