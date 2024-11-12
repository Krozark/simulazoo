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
    def __init__(self, specie: str):
        self.specie = specie
        self.hp = 10


class ZoophageComponent(RegisteredComponent):
    pass


class PhytophageComponent(RegisteredComponent):
    pass
