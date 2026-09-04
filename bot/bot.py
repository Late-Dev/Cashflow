#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
from dotenv import load_dotenv
import os
import re
import ast
import operator
from decimal import Decimal, InvalidOperation
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

EXPENSE_RE = re.compile(r"^\s*([0-9(][0-9\s+\-*/().,]*)\s+(.+?)\s*$")
EXPENSE_SEPARATOR_RE = re.compile(r"[\n]+|,\s+(?=[0-9(])")
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
pending_expenses = {}
user_languages = {}

LANGUAGES = {
    'en': 'English',
    'ru': 'Русский',
    'zh': '中文',
}

MESSAGES = {
    'en': {
        'choose_language': 'Please choose your language:',
        'language_saved': 'Language saved.',
        'open_wallet': 'Open your wallet',
        'switch_language': 'Change language',
        'language_inline_title': 'Set Cashflow language',
        'language_inline_description': 'Choose app and bot language',
        'help': """
Hello! Cashflow is an application for financial management and collaborative planning with your loved ones.

With Cashflow, you can:

<b>1. Track your expenses:</b> No more need for complicated spreadsheets. Cashflow allows you to easily record and monitor all your expenses in a user-friendly interface.

<b>2. Build savings:</b> Plan your savings and goals. Watch as your budget grows to achieve your dreams.

<b>3. Create shared wallets:</b> Invite your friends and family to shared wallets for joint financial management. Shared purchases or trips have become easier!

<b>4. Analyze finances:</b> Cashflow provides convenient reports and analytics to help you better understand where your money is going.

You can also write expenses in chat, for example: <code>2000 products</code>, <code>17+17 taxi</code>, or a list separated by commas/new lines.
""",
        'load_categories_error': 'Could not load expense categories. Please try again later.',
        'no_categories': 'No expense categories found for your default wallet.',
        'record_as': 'Record expense {amount} ({comment}) as:',
        'draft_expired': 'This expense draft expired. Please send it again.',
        'not_yours': 'This expense is not yours',
        'record_error': 'Could not record expense. Please try again.',
        'recorded': 'Recorded expense {amount}: {comment}',
    },
    'ru': {
        'choose_language': 'Пожалуйста, выберите язык:',
        'language_saved': 'Язык сохранён.',
        'open_wallet': 'Открыть кошелёк',
        'switch_language': 'Сменить язык',
        'language_inline_title': 'Выбрать язык Cashflow',
        'language_inline_description': 'Выберите язык приложения и бота',
        'help': """
Привет! Cashflow — приложение для управления финансами и совместного планирования с близкими.

С Cashflow можно:

<b>1. Отслеживать расходы:</b> больше не нужны сложные таблицы. Легко записывайте и контролируйте траты в удобном интерфейсе.

<b>2. Копить на цели:</b> планируйте накопления и цели, следите за ростом бюджета.

<b>3. Создавать общие кошельки:</b> приглашайте друзей и семью для совместного учёта расходов. Общие покупки и поездки становятся проще.

<b>4. Анализировать финансы:</b> отчёты и графики помогают понять, куда уходят деньги.

Также можно писать расходы прямо в чат, например: <code>2000 продукты</code>, <code>17+17 проезд</code>, или список через запятые/новые строки.
""",
        'load_categories_error': 'Не удалось загрузить категории расходов. Попробуйте позже.',
        'no_categories': 'В кошельке по умолчанию нет категорий расходов.',
        'record_as': 'Записать расход {amount} ({comment}) как:',
        'draft_expired': 'Черновик расхода устарел. Отправьте его ещё раз.',
        'not_yours': 'Этот расход не ваш',
        'record_error': 'Не удалось записать расход. Попробуйте ещё раз.',
        'recorded': 'Расход записан {amount}: {comment}',
    },
    'zh': {
        'choose_language': '请选择语言：',
        'language_saved': '语言已保存。',
        'open_wallet': '打开钱包',
        'switch_language': '切换语言',
        'language_inline_title': '设置 Cashflow 语言',
        'language_inline_description': '选择应用和机器人的语言',
        'help': """
你好！Cashflow 是一款用于财务管理和与亲友共同规划的应用。

使用 Cashflow 你可以：

<b>1. 记录支出：</b>不再需要复杂表格，可以在简洁界面中轻松记录和查看所有支出。

<b>2. 制定储蓄目标：</b>规划储蓄和目标，观察预算逐步增长。

<b>3. 创建共享钱包：</b>邀请朋友和家人一起管理财务，共同购物或旅行会更轻松。

<b>4. 分析财务：</b>通过报表和图表了解钱花在哪里。

你也可以直接在聊天中记录支出，例如：<code>2000 groceries</code>、<code>17+17 taxi</code>，或用逗号/换行分隔的列表。
""",
        'load_categories_error': '无法加载支出分类，请稍后重试。',
        'no_categories': '默认钱包没有支出分类。',
        'record_as': '将支出 {amount}（{comment}）记录为：',
        'draft_expired': '该支出草稿已过期，请重新发送。',
        'not_yours': '这不是你的支出',
        'record_error': '无法记录支出，请重试。',
        'recorded': '已记录支出 {amount}: {comment}',
    },
}


def api_url() -> str:
    return os.getenv('API_URL', '').rstrip('/')


def bot_secret() -> str:
    return os.getenv('BOT_SECRET', '')


def normalize_language(language: str | None) -> str | None:
    if not language:
        return None
    language = language.lower().replace('_', '-')
    if language.startswith('ru'):
        return 'ru'
    if language.startswith('zh') or language.startswith('cn'):
        return 'zh'
    if language.startswith('en'):
        return 'en'
    return None


def tr(language: str | None, key: str, **kwargs) -> str:
    lang = normalize_language(language) or 'en'
    return MESSAGES[lang][key].format(**kwargs)


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(label, callback_data=f'lang:{code}')
        for code, label in LANGUAGES.items()
    ]])


def start_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tr(language, 'open_wallet'), web_app={'url': os.getenv('WEBAPP_URL')})],
        [InlineKeyboardButton(tr(language, 'switch_language'), switch_inline_query_current_chat='language')],
    ])


def split_buttons(buttons, row_size=2):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]


def save_user_language(user_id: int, language: str) -> None:
    user_languages[user_id] = language
    response = requests.post(
        f"{api_url()}/bot_user_language/{user_id}",
        params={"secret": bot_secret()},
        json={"language": language},
        timeout=10,
    )
    response.raise_for_status()


def evaluate_amount(expression: str) -> Decimal:
    expression = expression.strip().replace(',', '.')
    if not expression or len(expression) > 80:
        raise ValueError("Invalid amount")
    if not re.fullmatch(r"[0-9\s+\-*/().]+", expression):
        raise ValueError("Invalid amount")

    def evaluate_node(node):
        if isinstance(node, ast.Expression):
            return evaluate_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate_node(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            left = evaluate_node(node.left)
            right = evaluate_node(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero")
            return ALLOWED_OPERATORS[type(node.op)](left, right)
        raise ValueError("Invalid amount")

    amount = evaluate_node(ast.parse(expression, mode='eval'))
    if amount <= 0:
        raise ValueError("Amount must be positive")
    return amount.quantize(Decimal('0.01')).normalize()


def format_amount(amount: Decimal) -> str:
    value = format(amount, 'f')
    if '.' in value:
        return value.rstrip('0').rstrip('.')
    return value


def parse_expense_items(text: str):
    expenses = []
    for raw_item in EXPENSE_SEPARATOR_RE.split(text):
        raw_item = raw_item.strip()
        if not raw_item:
            continue
        match = EXPENSE_RE.match(raw_item)
        if not match:
            raise ValueError(f"Could not parse: {raw_item}")
        try:
            amount = evaluate_amount(match.group(1))
        except (SyntaxError, ValueError, InvalidOperation) as exc:
            raise ValueError(f"Could not calculate amount: {match.group(1).strip()}") from exc
        expenses.append({
            'amount': format_amount(amount),
            'comment': match.group(2).strip(),
        })
    return expenses


async def send_start_info(message, language: str) -> None:
    await message.reply_html(
        tr(language, 'help'),
        reply_markup=start_keyboard(language),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not update.message or not user:
        return

    language = normalize_language(user.language_code)
    if language is None:
        await update.message.reply_text(tr('en', 'choose_language'), reply_markup=language_keyboard())
        return

    try:
        save_user_language(user.id, language)
    except Exception:
        logger.exception("Could not save user language")

    await send_start_info(update.message, language)


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return

    language = normalize_language(context.args[0]) if context.args else None
    if language:
        try:
            save_user_language(update.effective_user.id, language)
        except Exception:
            logger.exception("Could not save user language")
        await update.message.reply_html(tr(language, 'help'), reply_markup=start_keyboard(language))
        return

    await update.message.reply_text(tr('en', 'choose_language'), reply_markup=language_keyboard())


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.effective_user
    if not query or not query.data or not user:
        return

    await query.answer()
    _, language = query.data.split(':', 1)
    language = normalize_language(language) or 'en'

    try:
        save_user_language(user.id, language)
    except Exception:
        logger.exception("Could not save user language")

    await query.edit_message_text(tr(language, 'language_saved'))
    await query.message.reply_html(tr(language, 'help'), reply_markup=start_keyboard(language))


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    user = update.effective_user
    language = user_languages.get(user.id) or normalize_language(user.language_code) or 'en'

    if query.strip().lower() in {'language', 'lang', 'язык', '语言'}:
        results = [
            InlineQueryResultArticle(
                id=f'lang-{code}',
                title=f"{MESSAGES[language]['language_inline_title']}: {label}",
                description=MESSAGES[language]['language_inline_description'],
                input_message_content=InputTextMessageContent(f"/language {code}"),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=f'lang:{code}')]]),
            )
            for code, label in LANGUAGES.items()
        ]
        await update.inline_query.answer(results, cache_time=0, is_personal=True)
        return

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

    user_id = update.effective_user.id
    language = user_languages.get(user_id) or normalize_language(update.effective_user.language_code) or 'en'

    try:
        expenses = parse_expense_items(update.message.text)
    except ValueError:
        return

    if not expenses:
        return

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
        await update.message.reply_text(tr(language, 'load_categories_error'))
        return

    wallet = payload.get('wallet') or {}
    categories = payload.get('categories') or []
    if not categories:
        await update.message.reply_text(tr(language, 'no_categories'))
        return

    for expense in expenses:
        expense_id = uuid4().hex[:12]
        pending_expenses[expense_id] = {
            'user_id': user_id,
            'amount': expense['amount'],
            'comment': expense['comment'],
            'wallet_id': wallet.get('id'),
            'language': language,
        }

        buttons = [
            InlineKeyboardButton(
                f"{category.get('icon') or ''} {category.get('name')}",
                callback_data=f"expense:{expense_id}:{category.get('id')}",
            )
            for category in categories
        ]

        await update.message.reply_text(
            tr(language, 'record_as', amount=expense['amount'], comment=expense['comment']),
            reply_markup=InlineKeyboardMarkup(split_buttons(buttons)),
        )


async def expense_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    _, expense_id, category_id = query.data.split(':', 2)
    expense = pending_expenses.pop(expense_id, None)
    language = user_languages.get(update.effective_user.id) or (expense or {}).get('language') or normalize_language(update.effective_user.language_code) or 'en'

    if not expense:
        await query.edit_message_text(tr(language, 'draft_expired'))
        return

    if expense['user_id'] != update.effective_user.id:
        await query.answer(tr(language, 'not_yours'), show_alert=True)
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
        await query.edit_message_text(tr(language, 'record_error'))
        return

    await query.edit_message_text(tr(language, 'recorded', amount=expense['amount'], comment=expense['comment']))


def main() -> None:
    application = Application.builder().token(os.getenv('TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang:"))
    application.add_handler(CallbackQueryHandler(expense_category_callback, pattern=r"^expense:"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, record_expense_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
