CATEGORY_TRANSLATIONS = {
    'transport': {'en': 'Transport', 'ru': 'Транспорт', 'zh': '交通'},
    'food_dining': {'en': 'Food & Dining', 'ru': 'Еда и кафе', 'zh': '餐饮'},
    'shopping': {'en': 'Shopping', 'ru': 'Покупки', 'zh': '购物'},
    'healthcare': {'en': 'Healthcare', 'ru': 'Здоровье', 'zh': '医疗健康'},
    'education': {'en': 'Education', 'ru': 'Образование', 'zh': '教育'},
    'travel': {'en': 'Travel', 'ru': 'Путешествия', 'zh': '旅行'},
    'entertainment': {'en': 'Entertainment', 'ru': 'Развлечения', 'zh': '娱乐'},
    'utilities': {'en': 'Utilities', 'ru': 'Коммунальные услуги', 'zh': '水电杂费'},
    'gifts': {'en': 'Gifts', 'ru': 'Подарки', 'zh': '礼物'},
    'savings': {'en': 'Savings', 'ru': 'Сбережения', 'zh': '储蓄'},
    'rent': {'en': 'Rent', 'ru': 'Аренда', 'zh': '租金'},
    'loans': {'en': 'Loans', 'ru': 'Кредиты', 'zh': '贷款'},
    'subscriptions': {'en': 'Subscriptions', 'ru': 'Подписки', 'zh': '订阅'},
    'hobbies': {'en': 'Hobbies', 'ru': 'Хобби', 'zh': '爱好'},
    'investments': {'en': 'Investments', 'ru': 'Инвестиции', 'zh': '投资'},
    'miscellaneous': {'en': 'Miscellaneous', 'ru': 'Разное', 'zh': '其他'},
    'salary': {'en': 'Salary', 'ru': 'Зарплата', 'zh': '工资'},
    'freelance': {'en': 'Freelance', 'ru': 'Фриланс', 'zh': '自由职业'},
    'side_hustle': {'en': 'Side Hustle', 'ru': 'Подработка', 'zh': '副业'},
    'income_investments': {'en': 'Investments', 'ru': 'Инвестиции', 'zh': '投资收益'},
    'gifts_bonuses': {'en': 'Gifts & Bonuses', 'ru': 'Подарки и бонусы', 'zh': '礼物和奖金'},
    'property_sale': {'en': 'Property Sale', 'ru': 'Продажа имущества', 'zh': '资产出售'},
    'rental_income': {'en': 'Rental Income', 'ru': 'Доход от аренды', 'zh': '租金收入'},
    'income_miscellaneous': {'en': 'Miscellaneous', 'ru': 'Разное', 'zh': '其他收入'},
}

SUPPORTED_LANGUAGES = {'en', 'ru', 'zh'}


def normalize_language(language: str | None) -> str:
    if not language:
        return 'en'
    language = language.lower().replace('_', '-')
    if language.startswith('ru'):
        return 'ru'
    if language.startswith('zh') or language.startswith('cn'):
        return 'zh'
    return 'en'


def translate_category_name(default_key: str | None, language: str | None, fallback: str) -> str:
    if not default_key:
        return fallback
    return CATEGORY_TRANSLATIONS.get(default_key, {}).get(normalize_language(language), fallback)
