from random import randint

from snecs import RegisteredComponent

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
        self.hp = 10
        self.age = age or randint(0, 20)


class ZoophageComponent(RegisteredComponent):
    pass


class PhytophageComponent(RegisteredComponent):
    pass
