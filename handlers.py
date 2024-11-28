from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, filters
from utils import normalize_number

async def start(update, context):
    """Welcome message for the bot."""
    await update.message.reply_text(
        "⚡️ *Powered by @Rentt* ⚡️\n"
        "Send me a number to generate a link.\n"
        "Example: `+888 0888 0080` or `0888 0080`",
        parse_mode="Markdown",
    )

async def process_number(update, context):
    """Process the user's number and generate a link."""
    user_input = update.message.text.strip()
    normalized_number = normalize_number(user_input)

    # Generate the link
    link = f"https://fragment.com/number/{normalized_number}"

    # Create buttons: "Open in Fragment" and "Use Again"
    button_link = InlineKeyboardButton("Open in Fragment", url=link)
    button_restart = InlineKeyboardButton("🔄 Use Again", callback_data="restart")
    reply_markup = InlineKeyboardMarkup([[button_link], [button_restart]])

    await update.message.reply_text(
        f"⚡️ *Powered by @Rentt* ⚡️\n"
        f"Here is your link for `{normalized_number}`:\n{link}",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

async def inline_query(update, context):
    """Handle inline queries for the bot."""
    query = update.inline_query.query.strip()
    if query:
        # Normalize the number
        normalized_number = query.replace(" ", "").replace("+888", "")
        if not normalized_number.startswith("888"):
            normalized_number = "888" + normalized_number

        # Generate the Fragment.com link
        link = f"https://fragment.com/number/{normalized_number}"

        # Create the inline result
        result = InlineQueryResultArticle(
            id=normalized_number,
            title=f"Generate link for {normalized_number}",
            input_message_content=InputTextMessageContent(
                f"⚡️ *Powered by @Rentt* ⚡️\nHere is your link for {normalized_number}: {link}",
                parse_mode="Markdown"
            ),
        )

        # Respond to the query
        await update.inline_query.answer([result], cache_time=0)

async def restart(update, context):
    """Restart the process when 'Use Again' is clicked."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔄 Let's start again! Send me a number to generate a new link.",
    )

def setup_handlers(app):
    """Setup all bot handlers."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_number))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(restart, pattern="^restart$"))
