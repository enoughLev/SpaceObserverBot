from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from translator import translate_to_russian

# класс для inline кнопок избранного
class FavCallbackFactory(CallbackData, prefix="fav"):
    action: str
    index: int

# Клавиатура с основными командами
def make_start_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="/random")
    kb.button(text="/favorite_add")
    kb.button(text="/iss_status")
    kb.button(text="/iss_crew")
    kb.button(text="/help")
    kb.button(text="/favorites_list")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


# Inline клавиатура списка избранных объектов
def build_favorites_list_kb(favorites: list) -> InlineKeyboardMarkup:
    buttons = []
    for i, obj in enumerate(favorites):
        title = obj.get('title', 'Без названия')
        title_ru = translate_to_russian(title)  # Переводим название
        buttons.append([
            InlineKeyboardButton(
                text=f"{i + 1}. {title_ru}",
                callback_data=FavCallbackFactory(action="select", index=i).pack()
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text="🗑 Удалить все объекты из избранного",
            callback_data=FavCallbackFactory(action="delete_all", index=0).pack()
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Inline клавиатура для выбранного объекта
def build_favorite_object_kb(index: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text="🗑 Удалить данный объект",
            callback_data=FavCallbackFactory(action="delete", index=index).pack()
        )],
        [InlineKeyboardButton(
            text="📋 Посмотреть список избранных объектов",
            callback_data=FavCallbackFactory(action="list", index=0).pack()
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

