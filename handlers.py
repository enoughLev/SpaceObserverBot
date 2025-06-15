from aiogram import types
from buttons_worker import make_start_keyboard, build_favorites_list_kb, FavCallbackFactory, build_favorite_object_kb
from nasa_api import get_random_space_object
from scraper import get_iss_status, get_iss_crew
from favorites_actions import get_favorites, delete_favorite_by_index, add_to_favorites, delete_all_favorites
from logger import log_dialog
from translator import translate_to_russian

user_last_data = {}

# Хендлеры для кнопок

async def unknown_command_handler(event: types.Message):
    text = "Извините, я не знаю такую команду. Попробуйте /help для списка доступных команд."
    await event.answer(text)
    log_dialog(event.from_user.id, f'User: {event.text}\nBot: {text}')


async def start_handler(event: types.Message):
    try:
        with open("start.md", "r", encoding="utf-8") as f:
            start_text = f.read()
    except FileNotFoundError:
        start_text = "Файл start.md не найден."
    except Exception as e:
        start_text = f"Ошибка при чтении файла start.md: {e}"

    kb = make_start_keyboard()
    await event.answer(start_text, reply_markup=kb)
    log_dialog(event.from_user.id, f'User: {event.text}\nBot: {start_text}')


async def help_handler(event: types.Message):
    try:
        with open("help.md", "r", encoding="utf-8") as f:
            help_text = f.read()
    except FileNotFoundError:
        help_text = "Файл help.md не найден."
    except Exception as e:
        help_text = f"Ошибка при чтении файла help.md: {e}"

    kb = make_start_keyboard()
    await event.answer(help_text, reply_markup=kb)
    log_dialog(event.from_user.id, f'User: {event.text}\nBot: {help_text}')


async def random_handler(event: types.Message):
    data = get_random_space_object()
    user_last_data[event.from_user.id] = data
    if data:
        text = f"{translate_to_russian(data['title'])}\n\n{translate_to_russian(data['explanation'])}\n\n{data['url']}"
    else:
        text = "Не удалось получить данные с NASA API."
    kb = make_start_keyboard()
    await event.answer(text, reply_markup=kb)
    log_dialog(event.from_user.id, f'User: {event.text}\nBot: {text}')


async def iss_status_handler(event: types.Message):
    days = get_iss_status()
    text = f"МКС работает уже {days} дней."
    kb = make_start_keyboard()
    await event.answer(text, reply_markup=kb)
    log_dialog(event.from_user.id, f'User: {event.text}\nBot: {text}')


async def crew_handler(event: types.Message):
    crew = get_iss_crew()

    if not crew:
        await event.answer("Информация об экипаже временно недоступна.")
        return

    for member in crew:
        text = f"👨‍🚀 {member['name']}\nКоманда: {member['team']}"
        await event.answer(text)
        log_dialog(event.from_user.id, f'User: {event.text}\nBot: {text}')


async def favorite_add_handler(event: types.Message):
    user_id = event.from_user.id
    item = user_last_data.get(user_id)
    if item is None:
        text = "Сначала нужно выбрать объект"
        kb = make_start_keyboard()
        await event.answer(text, reply_markup=kb)
        return

    favorites = get_favorites(user_id)
    exists = any(fav.get('title') == item.get('title') for fav in favorites)
    if exists:
        text = "Этот объект уже есть в вашем избранном."
    else:
        add_to_favorites(user_id, item)
        text = "Объект добавлен в избранное."
    kb = make_start_keyboard()
    await event.answer(text, reply_markup=kb)

    log_dialog(user_id, f'User: {event.text}\nBot: {text}')


async def favorites_list_handler(event: types.Message):
    user_id = event.from_user.id
    favorites = get_favorites(user_id)
    if not favorites:
        await event.answer("Ваш список избранного пуст.", reply_markup=make_start_keyboard())
        return
    text = "Ваши избранные объекты. Выберите объект для просмотра:"
    kb = build_favorites_list_kb(favorites)
    await event.answer(text, reply_markup=kb)

    log_dialog(event.from_user.id, f'User: {event.text}\nBot: {text}')


# Хендлеры для inline кнопок избранного

async def favorites_callback_handler(call: types.CallbackQuery, callback_data: FavCallbackFactory):
    user_id = call.from_user.id
    action = callback_data.action
    index = callback_data.index
    favorites = get_favorites(user_id)

    if action == "list":
        if not favorites:
            await call.message.edit_text("Ваш список избранного пуст.")
            log_dialog(user_id, "User requested list: список пуст")
            await call.answer()
            return
        text = "Ваши избранные объекты. Выберите объект для просмотра:"
        kb = build_favorites_list_kb(favorites)
        await call.message.edit_text(text, reply_markup=kb)
        log_dialog(user_id, "User requested list: список показан")
        await call.answer()

    elif action == "select":
        if index < 0 or index >= len(favorites):
            await call.answer("Объект не найден.", show_alert=True)
            log_dialog(user_id, f"User tried to select invalid index {index}")
            return
        obj = favorites[index]
        title_ru = translate_to_russian(obj.get('title', 'Без названия'))
        explanation_ru = translate_to_russian(obj.get('explanation', 'Нет описания'))
        text = f"{title_ru}\n\n{explanation_ru}\n\n"
        if 'url' in obj:
            text += f"{obj['url']}"
        kb = build_favorite_object_kb(index)
        await call.message.edit_text(text, reply_markup=kb)
        await call.answer()

        log_dialog(user_id, f'User selected index {index}:\nBot response:\n{text}')

    elif action == "delete":
        if index < 0 or index >= len(favorites):
            await call.answer("Объект не найден.", show_alert=True)
            log_dialog(user_id, f"User tried to delete invalid index {index}")
            return
        success = delete_favorite_by_index(user_id, index)
        if success:
            favorites = get_favorites(user_id)
            if not favorites:
                await call.message.edit_text("Ваш список избранного пуст.")
                log_dialog(user_id, f"User deleted index {index}, список пуст")
            else:
                text = "Обновлённый список избранных объектов. Выберите объект для просмотра:"
                kb = build_favorites_list_kb(favorites)
                await call.message.edit_text(text, reply_markup=kb)
                log_dialog(user_id, f"User deleted index {index}, список обновлён")
        else:
            await call.message.edit_text("Ошибка при удалении объекта.")
            log_dialog(user_id, f"Ошибка при удалении объекта с индексом {index}")
        await call.answer()

    elif action == "delete_all":
        delete_all_favorites(user_id)
        await call.message.edit_text("Все объекты удалены из избранного.")
        log_dialog(user_id, "User deleted all favorites")
        await call.answer()
