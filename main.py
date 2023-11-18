import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, ExceptionTypeFilter

import config
from services.paste import extract_hash_from_paste_short_url
from exceptions import BotErrorException

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, я помогу тебе работать с пастами в Florgon CC.\n"
                         f"Пасты позволяют сохранить любой текст (например код) и позволяют "
                         f"передавать его. Для кода в пастах существует подсветка синтаксиса.")


@dp.message(Command("read"))
async def echo_handler(message: types.Message) -> None:
    """
    Takes url to paste and send paste text as a message.
    """
    paste_hash = extract_hash_from_paste_short_url(message.text)
    if paste_hash is None:
        message.reply(f"Ссылка должна быть в формате {config.URL_PASTE_OPEN_PROVIDER}/xxxxxx!")
        return


@dp.error(ExceptionTypeFilter(json.decoder.JSONDecodeError), F.update.message.as_("message"))
async def handle_json_exception(_: types.ErrorEvent, message: types.Message) -> None:
    await message.answer("Ошибка запроса! Свяжитесь с администрацией бота или повторите попытку.")


@dp.error(ExceptionTypeFilter(BotErrorException), F.update.message.as_("message"))
async def handle_bot_error(event: types.ErrorEvent, message: types.Message) -> None:
    await message.answer(event.exception.message)


async def main() -> None:
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
