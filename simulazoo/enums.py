from enum import Enum

__all__ = [
    "SexEnum",
]


class SexEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"
