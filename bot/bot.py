#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
from dotenv import load_dotenv
import os
import re
from datetime import datetime, timezone
from uuid import uuid4

import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

EXPENSE_RE = re.compile(r"^\s*(\d+(?:[\.,]\d+)?)\s+(.+?)\s*$")
pending_expenses = {}

help_string = rf"""
        
        Hello! Cashflow is an application for financial management and collaborative planning with your loved ones.

With Cashflow, you can:

<b>1. Track your expenses:</b> No more need for complicated spreadsheets. Cashflow allows you to easily record and monitor all your expenses in a user-friendly interface.

<b>2. Build savings:</b> Plan your savings and goals. Watch as your budget grows to achieve your dreams.

<b>3. Create shared wallets:</b> Invite your friends and family to shared wallets for joint financial management. Shared purchases or trips have become easier!

<b>4. Analyze finances:</b> Cashflow provides convenient reports and analytics to help you better understand where your money is going.

You can also write an expense in chat, for example: <code>2000 products</code> or <code>35 лепёшка</code>.
        """


def api_url() -> str:
    return os.getenv('API_URL', '').rstrip('/')


def bot_secret() -> str:
    return os.getenv('BOT_SECRET', '')


def split_buttons(buttons, row_size=2):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Open your wallet", web_app={'url': os.getenv('WEBAPP_URL')})]]
    await update.message.reply_html(
        help_string,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    user = update.effective_user
    if not query:
        return

    fetch_results = requests.get(
        f"{api_url()}/bot_user_wallets/{str(user.id)}",
        params={"secret": bot_secret()},
        timeout=10,
    )
    fetch_results.raise_for_status()
    wallet_list = fetch_results.json()

    results = [
        InlineQueryResultArticle(**{
            "id": str(wallet.get('id')),
            'title': wallet.get('name'),
            'input_message_content': InputTextMessageContent(
                f"{os.getenv('WEBAPP_TG_URL')}?startapp={wallet.get('link')}"
            )
        }) for wallet in wallet_list if query.lower() in wallet.get('name', '').lower()
    ]

    await update.inline_query.answer(results)


async def record_expense_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text or not update.effective_user:
        return

    match = EXPENSE_RE.match(update.message.text)
    if not match:
        return

    amount = match.group(1).replace(',', '.')
    comment = match.group(2).strip()
    user_id = update.effective_user.id

    try:
        response = requests.get(
            f"{api_url()}/bot_default_wallet/{user_id}/expense_categories",
            params={"secret": bot_secret()},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
    except Exception:
        logger.exception("Could not load expense categories")
        await update.message.reply_text("Could not load expense categories. Please try again later.")
        return

    wallet = payload.get('wallet') or {}
    categories = payload.get('categories') or []
    if not categories:
        await update.message.reply_text("No expense categories found for your default wallet.")
        return

    expense_id = uuid4().hex[:12]
    pending_expenses[expense_id] = {
        'user_id': user_id,
        'amount': amount,
        'comment': comment,
        'wallet_id': wallet.get('id'),
    }

    buttons = [
        InlineKeyboardButton(
            f"{category.get('icon') or ''} {category.get('name')}",
            callback_data=f"expense:{expense_id}:{category.get('id')}",
        )
        for category in categories
    ]

    await update.message.reply_text(
        f"record expense {amount} as:",
        reply_markup=InlineKeyboardMarkup(split_buttons(buttons)),
    )


async def expense_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    _, expense_id, category_id = query.data.split(':', 2)
    expense = pending_expenses.pop(expense_id, None)

    if not expense:
        await query.edit_message_text("This expense draft expired. Please send it again.")
        return

    if expense['user_id'] != update.effective_user.id:
        await query.answer("This expense is not yours", show_alert=True)
        return

    try:
        response = requests.post(
            f"{api_url()}/bot_transaction",
            params={"secret": bot_secret()},
            json={
                'user_id': expense['user_id'],
                'description': expense['comment'],
                'value': expense['amount'],
                'date': datetime.now(timezone.utc).isoformat(),
                'source': '',
                'category_id': int(category_id),
                'wallet_id': int(expense['wallet_id']),
            },
            timeout=10,
        )
        response.raise_for_status()
    except Exception:
        logger.exception("Could not record expense")
        await query.edit_message_text("Could not record expense. Please try again.")
        return

    await query.edit_message_text(f"Recorded expense {expense['amount']}: {expense['comment']}")


def main() -> None:
    application = Application.builder().token(os.getenv('TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CallbackQueryHandler(expense_category_callback, pattern=r"^expense:"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, record_expense_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
