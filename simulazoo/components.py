import random

import names
from snecs import Component, RegisteredComponent

from . import const
from .enums import SexEnum

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
    """
    Base component class that define serialization capabilities
    """
    def serialize(self):
        """
        Serialize component by dumping all its data
        :return: tuple containing all component data
        """
        return ()

    @classmethod
    def deserialize(cls, serialized: tuple):
        """
        Deserialize component.
        :param serialized: result of self.serialize()
        :return: A new component from serialized data
        """
        return cls()


################
## Components ##
################


class LivingBeingComponent(RegisteredComponent):
    """
    Component use for all living things, specifying specie, health and age
    """
    __slots__ = ("specie", "hp", "age")

    def __init__(self, specie: str, age: int = None, hp: int = None):
        """
        :param specie: The living being specie
        :param age: its age (default LIVING_BEING_DEFAULT_HP)
        :param hp: its health (default to a number between LIVING_BEING_MIN_AGE and LIVING_BEING_MAX_AGE)
        """
        self.specie = specie
        self.hp = hp or const.LIVING_BEING_DEFAULT_HP
        self.age = age or random.randint(
            const.LIVING_BEING_MIN_AGE, const.LIVING_BEING_MAX_AGE
        )

    def serialize(self):
        """
        Serialize component by dumping all its data

        :return: tuple containing all component data
        """
        return self.specie, self.age, self.hp

    @classmethod
    def deserialize(cls, serialized: tuple):
        """
        Deserialize component.

        :param serialized: result of self.serialize()
        :return: A new component from serialized data
        """
        return cls(*serialized)


class AnimalComponent(RegisteredComponent):
    """
    Component use for all animals things. specifying sex, and name
    """
    __slots__ = ("sex", "name")

    def __init__(self, name: str = None, sex: SexEnum = None):
        """
        :param name: the name on the animal. Default is pick at random
        :param sex:  The sex of the animal from SexEnum
        """
        if type(sex) is str:
            sex = SexEnum[sex]
        self.sex = sex if sex else random.choice([i for i in SexEnum])
        self.name = name or names.get_first_name(gender=self.sex.name.lower())

    def serialize(self):
        """
        Serialize component by dumping all its data

        :return: tuple containing all component data
        """
        return self.name, self.sex.name

    @classmethod
    def deserialize(cls, serialized: tuple):
        """
        Deserialize component.
        :param serialized: result of self.serialize()

        :return: A new component from serialized data
        """
        return cls(*serialized)


class PlantComponent(EmptyComponentBase, RegisteredComponent):
    """
    Component use for all plants with No data
    """
    pass


class ZoophageComponent(EmptyComponentBase, RegisteredComponent):
    """
    Component use for all Zoophage with No data
    """
    pass


class PhytophageComponent(EmptyComponentBase, RegisteredComponent):
    """
    Component use for all Phytophage with No data
    """
    pass
