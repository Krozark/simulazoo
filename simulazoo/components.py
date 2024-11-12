from random import randint

from snecs import RegisteredComponent
from . import const
from .enums import SexEnum

__all__ = [
    "AnimalComponent",
    "PlantComponent",
    "LivingBeingComponent",
    "ZoophageComponent",
    "PhytophageComponent",
]


class AnimalComponent(RegisteredComponent):
    def __init__(self, name: str, sex: SexEnum):
        self.name = name
        self.sex = sex


class PlantComponent(RegisteredComponent):
    pass


class LivingBeingComponent(RegisteredComponent):
    def __init__(self, specie: str, age: int = None):
        self.specie = specie
        self.hp = const.LIVING_BEING_DEFAULT_HP
        self.age = age or randint(
            const.LIVING_BEING_MIN_AGE, const.LIVING_BEING_MAX_AGE
        )


class ZoophageComponent(RegisteredComponent):
    pass


class PhytophageComponent(RegisteredComponent):
    pass
