import random

from snecs import Component, RegisteredComponent
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

##########
## Base ##
##########


class EmptyComponentBase(Component):
    def serialize(self):
        return ()

    @classmethod
    def deserialize(cls, serialized):
        return cls()


################
## Components ##
################


class LivingBeingComponent(RegisteredComponent):
    __slots__ = ("specie", "hp", "age")

    def __init__(self, specie: str, age: int = None, hp: int = None):
        self.specie = specie
        self.hp = hp or const.LIVING_BEING_DEFAULT_HP
        self.age = age or random.randint(
            const.LIVING_BEING_MIN_AGE, const.LIVING_BEING_MAX_AGE
        )

    def serialize(self):
        return self.specie, self.age, self.hp

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class AnimalComponent(RegisteredComponent):
    __slots__ = ("sex", "name")

    def __init__(self, name: str = None, sex: SexEnum = None):
        if type(sex) is str:
            sex = SexEnum[sex]
        self.sex = sex if sex else random.choice([i for i in SexEnum])
        self.name = name or names.get_first_name(gender=self.sex.name.lower())

    def serialize(self):
        return self.name, self.sex.name

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class PlantComponent(EmptyComponentBase, RegisteredComponent):
    pass


class ZoophageComponent(EmptyComponentBase, RegisteredComponent):
    pass


class PhytophageComponent(EmptyComponentBase, RegisteredComponent):
    pass
