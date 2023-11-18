"""
    Custom exceptions classes for different purposes.
"""

from typing import Self


class BotErrorException(Exception):
    """
    This exception class represents error in the bot,
    message should be answered to user.
    """
    DEFAULT_MESSAGE = "Произошла неизвестная ошибка! Попробуйте позже."

    def __init__(self: Self, message: str = DEFAULT_MESSAGE) -> None:
        super().__init__()
        self.message = message
