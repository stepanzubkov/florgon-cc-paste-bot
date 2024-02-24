"""
    Paste router (contains bot commands related to paste)
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

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Pre, Bold, as_marked_section, as_list

from services.paste import (
    extract_hash_from_paste_short_url,
    format_timedelta,
    get_paste_info_by_hash,
    expires_at_to_timedelta,
    format_timedelta,
    extract_paste_language_and_text_from_message,
    get_paste_stats_by_hash,
    get_url_for_paste,
    create_paste,
)

router = Router(name=__name__)


@router.message(Command("read"))
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


@router.message(Command("paste"))
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


@router.message(Command("stats"))
async def command_get_stats(message: types.Message) -> None:
    paste_hash = extract_hash_from_paste_short_url(message.text)
    success, response = await get_paste_stats_by_hash(paste_hash)
    if not success:
        await message.reply("Произошла ошибка: " + response["message"])
        return

    content = as_list(
        Bold(f"Всего просмотров: {response['views']['total']}\n"),
        as_marked_section(
            Bold("Просмотров по реферерам:"),
            *[f"{referer} - {value}%" for referer, value in response["views"]["by_referers"].items()],
        ),
        as_marked_section(
            Bold("Просмотров по датам:"),
            *[f"{date} - {value}%" for date, value in response["views"]["by_dates"].items()],
        )
    )

    await message.reply(**content.as_kwargs())

