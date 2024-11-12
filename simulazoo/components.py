import random

from snecs import Component, RegisteredComponent
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


class AnimalComponent(RegisteredComponent):
    def __init__(self, name: str = None, sex: SexEnum = None):
        self.sex = sex or random.choice([i for i in SexEnum])
        self.name = name or names.get_first_name(gender=self.sex.name.lower())

    def serialize(self):
        return self.sex, self.name

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class PlantComponent(EmptyComponentBase, RegisteredComponent):
    pass


class LivingBeingComponent(RegisteredComponent):
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


class ZoophageComponent(EmptyComponentBase, RegisteredComponent):
    pass


class PhytophageComponent(EmptyComponentBase, RegisteredComponent):
    pass
