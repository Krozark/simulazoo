from enum import Enum

__all__ = [
    "SexEnum",
]


class SexEnum(str, Enum):
    """
    Enum that contain sex Animals possibilities used
    """
    MALE = "M"
    FEMALE = "F"
