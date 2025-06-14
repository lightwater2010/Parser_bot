from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder



greeting_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Получить проекты"),
]], resize_keyboard=True)

async def get_categories(categories):
    categories_kb_builder = ReplyKeyboardBuilder()
    for category in categories:
        categories_kb_builder.add(KeyboardButton(text=category))
    return categories_kb_builder.adjust(4, repeat=True).as_markup()

skip_kb_builder_cat = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Пропустить", callback_data="skip_category")
    ]])

skip_kb_builder_price = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Пропустить", callback_data="skip_price")
    ]])

skip_kb_builder_date = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Пропустить", callback_data="skip_date")
    ]])

    
dates_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="За 1 день"),
    KeyboardButton(text="За неделю")], [KeyboardButton(text="За месяц")]
], resize_keyboard=True)
    
