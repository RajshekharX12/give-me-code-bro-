import random
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, filters, ApplicationBuilder

# Admin Telegram ID
ADMIN_ID = 5770074932  # Replace with your Telegram ID

# Inline text store (key-value pairs)
INLINE_TEXTS = {
    "A": "AAAA",
    "B": "BBBB"
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
    """Start command with Jarvis-like greetings for the admin."""
    if update.effective_user.id == ADMIN_ID:
        greeting = random.choice(GREETINGS)
        await update.message.reply_text(greeting)
    else:
        await update.message.reply_text(
            "Hello! Use me to generate links or fetch inline texts with @givecodebot."
        )

async def process_number(update, context):
    """Process the user's number and generate a link."""
    user_input = update.message.text.strip()
    normalized_number = user_input.replace(" ", "").replace("+888", "")
    if not normalized_number.startswith("888"):
        normalized_number = "888" + normalized_number

    # Generate the Fragment link
    link = f"https://fragment.com/number/{normalized_number}/code"

    await update.message.reply_text(link)

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
    elif query:
        # Inline query for number link
        normalized_number = query.replace(" ", "").replace("+888", "")
        if not normalized_number.startswith("888"):
            normalized_number = "888" + normalized_number

        link = f"https://fragment.com/number/{normalized_number}/code"
        result = InlineQueryResultArticle(
            id=normalized_number,
            title=f"Generate link for {normalized_number}",
            input_message_content=InputTextMessageContent(link)
        )
        await update.inline_query.answer([result], cache_time=0)
    else:
        await update.inline_query.answer([], cache_time=0)

async def add_text(update, context):
    """Admin command to add a new inline text."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized access!")
        return

    if not context.args or "|" not in context.args[0]:
        await update.message.reply_text("Provide text in the format: `<key>|<text>`.")
        return

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_number))
    app.add_handler(InlineQueryHandler(inline_query))

if __name__ == "__main__":
    # Replace with your bot token
    bot_token = "YOUR_BOT_TOKEN"
    application = ApplicationBuilder().token(bot_token).build()

    setup_handlers(application)
    application.run_polling()
