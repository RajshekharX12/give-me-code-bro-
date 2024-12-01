from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, filters
from transformers import pipeline
from utils import normalize_number
import os

# Load the Hugging Face conversational model
conversation_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

async def start(update, context):
    """Welcome message for the bot."""
    await update.message.reply_text(
        "⚡️ *Powered by @Rentt* ⚡️\n"
        "Send me a number to generate a link.\n"
        "Use `@givecodebot jr <text>` or `/jr <text>` for smart replies!",
        parse_mode="Markdown",
    )

async def process_number(update, context):
    """Process the user's number and generate a link."""
    user_input = update.message.text.strip()
    normalized_number = normalize_number(user_input)

    # Generate the link
    link = f"https://fragment.com/number/{normalized_number}/code"

    # Only display the link
    await update.message.reply_text(
        f"{link}",
    )

async def inline_query(update, context):
    """Handle inline queries for the bot."""
    query = update.inline_query.query.strip()
    if query.startswith("jr "):
        # Jarvis-style response using Hugging Face
        user_input = query[3:]  # Remove "jr " prefix
        reply = generate_ai_response(user_input)
        result = InlineQueryResultArticle(
            id="jarvis-response",
            title="Jarvis Reply",
            input_message_content=InputTextMessageContent(reply)
        )
        await update.inline_query.answer([result], cache_time=0)
    elif query:
        # Normal number processing
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

async def jarvis_reply(update, context):
    """Handle Jarvis-like replies in chat."""
    user_input = " ".join(context.args)  # Get text after "jr"
    if not user_input:
        await update.message.reply_text("What can I assist you with?")
        return
    reply = generate_ai_response(user_input)
    await update.message.reply_text(reply)

def generate_ai_response(prompt):
    """Generate a response using the Hugging Face FLAN-T5 model."""
    try:
        response = conversation_pipeline(prompt, max_length=100, num_return_sequences=1)
        return response[0]["generated_text"]
    except Exception as e:
        return f"Oops! Something went wrong: {e}"

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
    app.add_handler(CommandHandler("jr", jarvis_reply))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(restart, pattern="^restart$"))
