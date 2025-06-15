import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import config
import handlers

print("Please, enter your bot token: ", end='')
config.BOT_TOKEN = input()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

async def main():
    # Регистрируем обработчики команд
    dp.message.register(handlers.start_handler, Command(commands=["start"]))
    dp.message.register(handlers.random_handler, Command(commands=["random"]))
    dp.message.register(handlers.iss_status_handler, Command(commands=["iss_status"]))
    dp.message.register(handlers.favorite_add_handler, Command(commands=["favorite_add"]))
    dp.message.register(handlers.help_handler, Command(commands=["help"]))
    dp.message.register(handlers.favorites_list_handler, Command(commands=["favorites_list"]))
    dp.message.register(handlers.crew_handler, Command(commands=["iss_crew"]))
    dp.message.register(
        handlers.unknown_command_handler,
        lambda message: message.text and message.text.startswith('')
    )

    dp.callback_query.register(handlers.favorites_callback_handler, handlers.FavCallbackFactory.filter())

    print("Cool, token is valid. The bot is running!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
