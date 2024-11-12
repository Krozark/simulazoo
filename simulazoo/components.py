import random

from snecs import RegisteredComponent
from . import const
from .enums import SexEnum
import names

__all__ = [
    "LivingBeingComponent",
    "AnimalComponent",
    "PlantComponent",
    "ZoophageComponent",
    "PhytophageComponent",
]


class LivingBeingComponent(RegisteredComponent):
    __slots__ = ("specie", "hp", "age")

    def __init__(self, specie: str, age: int = None):
        self.specie = specie
        self.hp = const.LIVING_BEING_DEFAULT_HP
        self.age = age or random.randint(
            const.LIVING_BEING_MIN_AGE, const.LIVING_BEING_MAX_AGE
        )


class AnimalComponent(RegisteredComponent):
    __slots__ = ("sex", "name")

    def __init__(self, name: str = None, sex: SexEnum = None):
        self.sex = SexEnum[sex] if sex else random.choice([i for i in SexEnum])
        self.name = name or names.get_first_name(gender=self.sex.name.lower())


class PlantComponent(RegisteredComponent):
    pass


class ZoophageComponent(RegisteredComponent):
    pass


class PhytophageComponent(RegisteredComponent):
    pass
