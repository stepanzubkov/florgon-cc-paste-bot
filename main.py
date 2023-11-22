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
from aiogram.filters import CommandStart, Command, ExceptionTypeFilter
from aiogram.utils.formatting import Text, Pre

import config
from services.paste import (
    extract_hash_from_paste_short_url,
    format_timedelta,
    get_paste_info_by_hash,
    expires_at_to_timedelta,
    format_timedelta,
    extract_paste_language_and_text_from_message,
    get_url_for_paste,
    create_paste,
)
from exceptions import BotErrorException

dp = Dispatcher()


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


@dp.message(Command("read"))
async def command_read_paste(message: types.Message) -> None:
    """
    Takes url to paste and send paste text as a message.
    """
    paste_hash = extract_hash_from_paste_short_url(message.text)
    success, response = await get_paste_info_by_hash(paste_hash)
    if not success:
        await message.reply("Произошла ошибка: " + response["message"])
        return

    if response["is_expired"]:
        await message.reply("Срок действия пасты истёк!")
        return

    expires_timedelta = expires_at_to_timedelta(response["expires_at"])
    content = Text(
        f"Срок действия пасты истечёт через {format_timedelta(expires_timedelta)}",
        Pre(response["text"], language=response["language"]),
    )
    await message.reply(**content.as_kwargs())


@dp.message(Command("paste"))
async def command_create_paste(message: types.Message) -> None:
    language, text = extract_paste_language_and_text_from_message(message.html_text)
    success, response = await create_paste(
        text=text,
        language=language,
    )
    if not success:
        await message.reply("Произошла ошибка: ", response["message"])
        return

    await message.reply(f"Готово! {get_url_for_paste(response['hash'])}")


@dp.error(
    ExceptionTypeFilter(json.decoder.JSONDecodeError), F.update.message.as_("message")
)
async def handle_json_exception(_: types.ErrorEvent, message: types.Message) -> None:
    await message.reply(
        "Ошибка запроса! Свяжитесь с администрацией бота или повторите попытку."
    )


@dp.error(ExceptionTypeFilter(BotErrorException), F.update.message.as_("message"))
async def handle_bot_error(event: types.ErrorEvent, message: types.Message) -> None:
    await message.reply(event.exception.message)


async def main() -> None:
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
