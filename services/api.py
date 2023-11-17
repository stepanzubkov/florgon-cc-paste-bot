import httpx

from typing import Dict, Union, NoReturn, Optional, Any

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
        response = client.request(
            http_method,
            request_url,
            json=data,
            params=params,
            headers={"Authorization": access_token} if access_token else {},
        )

    return await response


def get_api_host() -> str:
    """
    Returns API host from user config. If it is not set, returns default API host.
    :rtype: str
    :return: API host
    """
    return config.CC_API_URL


def try_decode_response_to_json(response: httpx.Response) -> Union[Dict[str, Any], NoReturn]:
    """
    Tries to decode response to json.
    :param requests.Response response: response object
    :return: JSON dict if decoding is successfully, else exit application
    :rtype: Union[Dict[str, Any], NoReturn]
    """
    return response.json()

