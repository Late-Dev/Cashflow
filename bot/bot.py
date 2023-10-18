#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from dotenv import load_dotenv
import os 
from uuid import uuid4
from html import escape

import requests

from telegram.constants import ParseMode
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, InlineQueryHandler

load_dotenv()
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


help_string = rf"""
        
        Hello! Cashflow is an application for financial management and collaborative planning with your loved ones.

With Cashflow, you can:

<b>1. Track your expenses:</b> No more need for complicated spreadsheets. Cashflow allows you to easily record and monitor all your expenses in a user-friendly interface.

<b>2. Build savings:</b> Plan your savings and goals. Watch as your budget grows to achieve your dreams.

<b>3. Create shared wallets:</b> Invite your friends and family to shared wallets for joint financial management. Shared purchases or trips have become easier!

<b>4. Analyze finances:</b> Cashflow provides convenient reports and analytics to help you better understand where your money is going and how to save.
        """


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Open your wallet", web_app={'url': os.getenv('WEBAPP_URL')}),
        ],

    ]
    await update.message.reply_html(
        help_string,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    user = update.effective_user
    if not query:  # empty query should not be handled
        return

    fetch_results = requests.get(f"{os.getenv('API_URL')}/bot_user_wallets/{str(user.id)}?secret={os.getenv('BOT_SECRET')}")

    wallet_list = fetch_results.json()

    results = [
        InlineQueryResultArticle(**{
            "id": wallet.get('id'),
            'title': wallet.get('name'),
            'input_message_content': InputTextMessageContent( f"{os.getenv('WEBAPP_TG_URL')}?startapp={wallet.get('link')}")
        }) for wallet in wallet_list if query.lower() in wallet.get('name').lower()
    ]
    
    await update.inline_query.answer(results)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()