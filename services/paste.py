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
from typing import Literal, NoReturn

import config
from exceptions import BotErrorException
from services.api import execute_json_api_method
from models import Error, Paste


async def get_paste_info_by_hash(hash: str) -> tuple[Literal[True], Paste] | tuple[Literal[False], Error]:
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
        response["success"]["paste"]["text"] = response["success"]["paste"]["text"].replace(
            "\\n", "\n"
        )
        return True, response["success"]["paste"]
    return False, response["error"]


def extract_hash_from_paste_short_url(short_url: str) -> str | NoReturn:
    """
    Extracts hash from paste short url.
    :param str short_url: paste short url
    :rtype: str | None
    :return: paste hash or None if invalid short_url
    """
    short_url_hashes = re.findall(
        f"{config.URL_PASTE_OPEN_PROVIDER}" + r"/([a-zA-Z0-9]{6})", short_url
    )
    if not short_url_hashes:
        raise BotErrorException(
            f"Ссылка должна быть в формате {config.URL_PASTE_OPEN_PROVIDER}/xxxxxx!",
        )

    return short_url_hashes[0]
