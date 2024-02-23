"""
    Custom exceptions classes for different purposes.
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

from typing import Self


class ServiceErrorException(Exception):
    """
    This exception class represents error in the service,
    message should be answered to user.
    """

    DEFAULT_MESSAGE = "Произошла неизвестная ошибка! Попробуйте позже."

    def __init__(self: Self, message: str = DEFAULT_MESSAGE) -> None:
        super().__init__()
        self.message = message


class HashNotFoundException(ServiceErrorException):
    pass


class CodeBlockNotFoundException(ServiceErrorException):
    pass
