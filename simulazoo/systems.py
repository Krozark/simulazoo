import random
from copy import deepcopy

import names
from snecs import Query, entity_component, new_entity, schedule_for_deletion

from . import const
from .components import (
    AnimalComponent,
    LivingBeingComponent,
    PhytophageComponent,
    PlantComponent,
    ZoophageComponent,
)
from .enums import SexEnum

__all__ = [
    "LivingBeingSystem",
    "PlantSystem",
    "AnimalSystem",
    "ZoophageSystem",
    "PhytophageSystem",
]

###########
## Bases ##
###########


class SystemBase:
    """
    Base system for ECS
    """

    COMPONENTS = () # component to query

    def process(self, world):
        """
        Query the world to get the entity to process

        :param world: word to query
        """
        for entity, components in Query(component_types=self.COMPONENTS, world=world):
            self.process_entity(entity, components, world)

    def process_entity(self, entity, components, world):
        """
        Here is where the logic of the system happen for an entity.

        :param entity: Entity to process
        :param components: components instances of the entity in same order and type as COMPONENTS
        :param world: world queried
        """
        raise NotImplementedError


class _DietBaseSystem(SystemBase):
    """"
    System that manage diet
    """

    # COMPONENTS eat DIET
    DIET = (LivingBeingComponent,)

    def process(self, world):
        """
        Query the world to get the entity to process and search for potential pray
        stored into self.entity_targeted. This allows to avoid querying newly created entity and querying multiple times.

        :param world: word te query
        """
        self.entity_targeted = {
            entity: components
            for entity, components in Query(component_types=self.DIET, world=world)
        }
        super().process(world)

    def process_entity(self, entity, components, world):
        """
        Here is where the logic of the system happen for an entity.
        Check if the entity need to eat then pick a pray at random (excluding itself and its specie)

        :param entity: Entity to process
        :param components: components instances of the entity in same order and type as COMPONENTS
        :param world: world queried
        """

        living_being_cmp = components[0]
        if living_being_cmp.hp > const.ANIMAL_HUNGER_THRESHOLD:
            # no need to feed today
            return

        # remove same specie as valid choice (this includes the current entity)
        invalid_entity = {
            entity
            for entity in self.entity_targeted
            if entity_component(entity, LivingBeingComponent, world=world).specie
            == living_being_cmp.specie
        }
        # build valid food choice list
        food_choices = self.entity_targeted.keys() - invalid_entity
        if food_choices:
            entity_to_eat = random.choice(list(food_choices))
            self.eat(components, self.entity_targeted[entity_to_eat], world)

    def eat(self, components, target_components, world):
        """
        Do somthing with a validated pray.

        :param components: components instances of the entity in same order and type as COMPONENTS.
        :param target_components: components instances of the entity targeted in same order and type as COMPONENTS.
        :param world: world queried
        """
        raise NotImplementedError


##################
## Real systems ##
##################


class LivingBeingSystem(SystemBase):
    """"
    System that manage death and ageing.
    """

    COMPONENTS = (LivingBeingComponent,)

    def process_entity(self, entity, components, world):
        """
        Here is where the logic of the system happen for an entity.
        Increase the age of the entity by one, and delete it from the word if too old.

        :param entity: Entity to process
        :param components: components instances of the entity in same order and type as COMPONENTS
        :param world: world queried
        """

        living_being_cmp = components[0]
        living_being_cmp.age += const.LIVING_BEING_DAILY_INC_AGE
        if (
            living_being_cmp.hp <= const.LIVING_BEING_DEATH_THRESHOLD
            or living_being_cmp.age > const.LIVING_BEING_MAX_AGE
        ):
            schedule_for_deletion(entity, world=world)


class PlantSystem(SystemBase):
    """"
    System that manage plants.
    """

    COMPONENTS = (
        LivingBeingComponent,
        PlantComponent,
    )

    def process_entity(self, entity, components, world):
        """
        Here is where the logic of the system happen for an entity.
        Manage regeneration and plant splitting.

        :param entity: Entity to process
        :param components: components instances of the entity in same order and type as COMPONENTS
        :param world: world queried
        """

        self._daily_regeneration(components)
        self._maybe_split_plant(components, world)

    @staticmethod
    def _daily_regeneration(components):
        living_being_cmp = components[0]
        living_being_cmp.hp += const.PLANT_DAILY_REGENERATION

    @staticmethod
    def _maybe_split_plant(components, world):
        living_being_cmp = components[0]

        if living_being_cmp.hp <= const.PLANT_SPLIT_THRESHOLD:
            return

        # Let’s make a new plant
        new_components = [deepcopy(component) for component in components]
        new_living_being_cmp = new_components[0]
        # set age and HP
        new_living_being_cmp.hp //= 2  # split HP in halp round down
        new_living_being_cmp.age = const.LIVING_BEING_BABY_AGE
        # add it to the wold
        new_entity(components=new_components, world=world)
        # subtract hp lost during division
        living_being_cmp.hp -= new_living_being_cmp.hp


class AnimalSystem(SystemBase):
    """"
    System that manage Animals.
    """

    COMPONENTS = (
        LivingBeingComponent,
        AnimalComponent,
    )

    def process(self, world):
        """
        Query the world to get the entity to process and store them
        into initial animal list to avoid babys. This will also help us for partner finding

        :param world: word to query
        """

        self.animals = list(Query(component_types=self.COMPONENTS, world=world))
        for entity, components in self.animals:
            self.process_entity(entity, components, world)

    def process_entity(self, entity, components, world):
        """
        Here is where the logic of the system happen for an entity.
        Manage regeneration and reproduction.

        :param entity: Entity to process
        :param components: components instances of the entity in same order and type as COMPONENTS
        :param world: world queried
        """

        self._daily_regeneration(components)
        self._maybe_reproduce(entity, components, world)

    @staticmethod
    def _daily_regeneration(components):
        living_being_cmp = components[0]
        living_being_cmp.hp += const.ANIMAL_DAILY_REGENERATION

    def _maybe_reproduce(self, entity, components, world):
        living_being_cmp = components[0]

        if living_being_cmp.hp <= const.ANIMAL_HUNGER_THRESHOLD:
            # need to feed today, no time for that
            return

        # no need to feed today, let find a partner to make a baby
        # first, let’s try to find a partner
        partners = [
            (it_entity, it_components)
            for it_entity, it_components in self.animals
            if it_entity != entity
        ]
        if not partners:
            return

        partner_id, (partner_living_being_cmp, partner_animal_cmp) = random.choice(
            partners
        )
        animal_cmp = components[1]
        # let’s check if this animal is same species and different sex
        if (
            living_being_cmp.specie == partner_living_being_cmp.specie
            and animal_cmp.sex != partner_animal_cmp.sex
        ):
            # make a baby
            new_components = [deepcopy(component) for component in components]
            new_living_being_cmp, new_animal_cmp = new_components
            # set age and HP
            new_living_being_cmp.hp = const.LIVING_BEING_DEFAULT_HP
            new_living_being_cmp.age = const.LIVING_BEING_BABY_AGE
            # set sex and name
            new_animal_cmp.sex = random.choice([i for i in SexEnum])
            new_animal_cmp.name = names.get_first_name(
                gender=new_animal_cmp.sex.name.lower()
            )

            # add it to the wold
            new_entity(components=new_components, world=world)


class ZoophageSystem(_DietBaseSystem):
    # ZoophageComponent eat AnimalComponent
    COMPONENTS = (
        LivingBeingComponent,
        ZoophageComponent,
    )
    DIET = (
        *_DietBaseSystem.DIET,
        AnimalComponent,
    )

    def eat(self, components, target_components, world):
        """
        Eat the pray.

        :param components: components instances of the entity in same order and type as COMPONENTS.
        :param target_components: components instances of the entity targeted in same order and type as COMPONENTS.
        :param world: world queried
        """

        # zoophage gain 5 HP by eating;
        components[0].hp += const.ZOOPHAGE_RECOVERY_AFTER_EATING
        # animals loose 4 HP when eaten
        target_components[0].hp -= const.ANIMAL_LIFE_LOST_FROM_ATTACK


class PhytophageSystem(_DietBaseSystem):
    # PhytophageComponent eat PlantComponent
    COMPONENTS = (
        LivingBeingComponent,
        PhytophageComponent,
    )
    DIET = (
        *_DietBaseSystem.DIET,
        PlantComponent,
    )

    def eat(self, components, target_components, world):
        """
        Eat the plant.

        :param components: components instances of the entity in same order and type as COMPONENTS.
        :param target_components: components instances of the entity targeted in same order and type as COMPONENTS.
        :param world: world queried
        """

        # Phytophage gain 3 HP by eating;
        components[0].hp += const.PHYTOPHAGE_RECOVERY_AFTER_EATING
        # plant loose 2 HP when eaten
        target_components[0].hp -= const.PLANT_LIFE_LOST_FROM_ATTACK
