"""
    Main executable file.
    Copyright (C) 2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, ExceptionTypeFilter

import config
from routers import routers
from exceptions import ServiceErrorException

dp = Dispatcher()
dp.include_routers(*routers)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Привет, я помогу тебе работать с пастами в Florgon CC.\n"
        f"Пасты позволяют сохранить любой текст (например код) и позволяют "
        f"передавать его. Для кода в пастах существует подсветка синтаксиса."
    )


@dp.error(
    ExceptionTypeFilter(json.decoder.JSONDecodeError), F.update.message.as_("message")
)
async def handle_json_exception(_: types.ErrorEvent, message: types.Message) -> None:
    await message.reply(
        "Ошибка запроса! Свяжитесь с администрацией бота или повторите попытку."
    )


@dp.error(ExceptionTypeFilter(ServiceErrorException), F.update.message.as_("message"))
async def handle_bot_error(event: types.ErrorEvent, message: types.Message) -> None:
    await message.reply(event.exception.message)


async def main() -> None:
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
