"""
    Services for pastes.
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

import re
import html
from typing import Literal, NoReturn
from datetime import timedelta
import time

from config import settings
from exceptions import CodeBlockNotFoundException, HashNotFoundException
from services.api import execute_json_api_method
from models import Error, Paste, Stats


async def get_paste_info_by_hash(
    hash: str,
) -> tuple[Literal[True], Paste] | tuple[Literal[False], Error]:
    """
    Returns info about paste short url by hash.
    :param str hash: short url hash
    :return: Tuple with two elements.
             First is a response status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[True, Paste] if request is successfully, else Tuple[True, Error]
    """
    response = await execute_json_api_method("GET", f"pastes/{hash}/")
    if "success" in response:
        response["success"]["paste"]["text"] = response["success"]["paste"][
            "text"
        ].replace("\\n", "\n")
        return True, response["success"]["paste"]
    return False, response["error"]


async def create_paste(
    text: str, language: str,
) -> tuple[Literal[True], Paste] | tuple[Literal[False], Error]:
    response = await execute_json_api_method("POST", "pastes/", data={
        "text": text, "language": language, "stats_is_public": True,
    })
    if "success" in response:
        return True, response["success"]["paste"]
    return False, response["error"]


async def get_paste_stats_by_hash(
    hash: str
) -> tuple[Literal[True], Stats] | tuple[Literal[False], Error]:
    """
    Returns stats about paste short url by hash.
    :param str hash: short url hash
    :return: Tuple with two elements.
             First is a response status (True if successfully).
             Seconds is a response body.
    :rtype: Tuple[True, Paste] if request is successfully, else Tuple[True, Error]
    """
    response = await execute_json_api_method("GET", f"pastes/{hash}/stats")
    if "success" in response:
        return True, response["success"]
    return False, response["error"]


def extract_hash_from_paste_short_url(short_url: str) -> str | NoReturn:
    """
    Extracts hash from paste short url.
    :param str short_url: paste short url
    :rtype: str | None
    :return: paste hash or None if invalid short_url
    """
    short_url_hashes = re.findall(
        f"{settings.url_paste_open_provider}" + r"/([a-zA-Z0-9]{6})", short_url
    )
    if not short_url_hashes:
        raise HashNotFoundException(
            f"Ссылка должна быть в формате {settings.url_paste_open_provider}/xxxxxx!",
        )

    return short_url_hashes[0]


def extract_paste_language_and_text_from_message(message: str) -> tuple[str, str]:
    text = re.findall(
        "<pre>(.*)</pre>", message, re.DOTALL
    )
    if not text:
        raise CodeBlockNotFoundException(
            "Сообщение должно содержать блок текста, заключённый в обратные ковычки."
        )
    text = text[0]
    result = re.findall(
        r'<code class="language-(\w+)">(.*)</code>', text, re.DOTALL
    )
    if not result:
        return "plain", html.unescape(text)
    return html.unescape(result[0])


def expires_at_to_timedelta(expires_at: int) -> timedelta:
    """
    Converts expires_at to timedelta.
    :param int expires_at: timestamp
    :return: timedelta
    :rtype: timedelta
    """
    return timedelta(seconds=expires_at - time.time())


def format_timedelta(td: timedelta) -> str:
    """
    Formats timedelta object to human readable view.
    :param timedelta td: timedelta object
    :return: timedelta as string
    :rtype: str
    """
    if td.days % 10 == 1:
        days_plural = "день"
    elif td.days % 10 in (2, 3, 4) and td.days % 100 not in [12, 13, 14]:
        days_plural = "дня"
    else:
        days_plural = "дней"

    return f"{td.days} {days_plural}"


def get_url_for_paste(hash: str) -> str:
    return f"{settings.url_paste_open_provider}/{hash}"
