import random

from snecs import RegisteredComponent
from . import const
from .enums import SexEnum
import names

__all__ = [
    "AnimalComponent",
    "PlantComponent",
    "LivingBeingComponent",
    "ZoophageComponent",
    "PhytophageComponent",
]


class AnimalComponent(RegisteredComponent):
    def __init__(self, name: str = None, sex: SexEnum = None):
        self.sex = sex or random.choice([i for i in SexEnum])
        self.name = name or names.get_first_name(gender=self.sex.name.lower())


class PlantComponent(RegisteredComponent):
    pass


class LivingBeingComponent(RegisteredComponent):
    def __init__(self, specie: str, age: int = None):
        self.specie = specie
        self.hp = const.LIVING_BEING_DEFAULT_HP
        self.age = age or random.randint(
            const.LIVING_BEING_MIN_AGE, const.LIVING_BEING_MAX_AGE
        )


class ZoophageComponent(RegisteredComponent):
    pass


class PhytophageComponent(RegisteredComponent):
    pass
