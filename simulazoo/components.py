from enum import Enum

from snecs import RegisteredComponent


class SexEnum(Enum):
    MALE = "M"
    FEMALE = "F"


class AnimalComponent(RegisteredComponent):
    def __init__(self, name: str, sex: SexEnum):
        self.name = name
        self.sex = sex

    def __str__(self):
        return f"{self.name} {self.sex}"


class PlantComponent(RegisteredComponent):
    pass
