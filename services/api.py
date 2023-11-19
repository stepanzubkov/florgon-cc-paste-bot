"""
    General services for communicating with Florgon CC API.
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
from typing import Dict, Union, NoReturn, Optional, Any

import httpx

import config


async def execute_json_api_method(
    http_method: str,
    api_method: str,
    *,
    data: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    access_token: Optional[str] = None,
) -> Union[Dict[str, Any], NoReturn]:
    """
    Executes API method.
    :param str http_method: GET, POST, PUT, PATCH, DELETE or OPTIONS
    :param str api_method: API method, described in docs
    :param Dict[str, Any] data: POST JSON data
    :param Dict[str, Any] params: GET data
    :param Optional[str] access_token: Florgon OAuth token
    :rtype: Union[Dict[str, Any], NoResponse]
    :return: JSON response from API or exit application
    """
    response = await execute_api_method(
        http_method,
        api_method,
        data=data,
        params=params,
        access_token=access_token,
    )
    return try_decode_response_to_json(response)


async def execute_api_method(
    http_method: str,
    api_method: str,
    *,
    data: Dict[str, Any] = {},
    params: Dict[str, Any] = {},
    access_token: Optional[str] = None,
) -> httpx.Response:
    """
    Executes API method and returns Request object.
    :param str http_method: GET, POST, PUT, PATCH, DELETE or OPTIONS
    :param str api_method: API method, described in docs
    :param Dict[str, Any] data: POST JSON data
    :param Dict[str, Any] params: GET data
    :param Optional[str] access_token: Florgon OAuth token
    :rtype: requests.Response
    :return: response object
    """
    request_url = f"{get_api_host()}/{api_method}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            http_method,
            request_url,
            json=data,
            params=params,
            headers={"Authorization": access_token} if access_token else {},
        )

    return response


def get_api_host() -> str:
    """
    Returns API host from user config. If it is not set, returns default API host.
    :rtype: str
    :return: API host
    """
    return config.CC_API_URL


def try_decode_response_to_json(
    response: httpx.Response,
) -> Union[Dict[str, Any], NoReturn]:
    """
    Tries to decode response to json.
    :param requests.Response response: response object
    :return: JSON dict if decoding is successfully, else exit application
    :rtype: Union[Dict[str, Any], NoReturn]
    """
    return response.json()
