import random

import names
from snecs import Query, entity_component, new_entity, schedule_for_deletion
from . import const
from copy import deepcopy
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
    COMPONENTS = ()

    def process(self, world):
        for entity, components in Query(component_types=self.COMPONENTS, world=world):
            self.process_entity(entity, components, world)

    def process_entity(self, entity, components, world):
        raise NotImplementedError


class _DietBaseSystem(SystemBase):
    # system that manage diet
    # COMPONENTS eat DIET
    DIET = (LivingBeingComponent,)

    def process(self, world):
        self.entity_targeted = {
            entity: components
            for entity, components in Query(component_types=self.DIET, world=world)
        }
        super().process(world)

    def process_entity(self, entity, components, world):
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
        raise NotImplementedError


##################
## Real systems ##
##################


class LivingBeingSystem(SystemBase):
    COMPONENTS = (LivingBeingComponent,)

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        living_being_cmp.age += const.LIVING_BEING_DAILY_INC_AGE
        if (
            living_being_cmp.hp <= const.LIVING_BEING_DEATH_THRESHOLD
            or living_being_cmp.age > const.LIVING_BEING_MAX_AGE
        ):
            schedule_for_deletion(entity, world=world)


class PlantSystem(SystemBase):
    COMPONENTS = (
        LivingBeingComponent,
        PlantComponent,
    )

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        living_being_cmp.hp += const.PLANT_DAILY_REGENERATION

        if living_being_cmp.hp > const.PLANT_SPLIT_THRESHOLD:
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
    COMPONENTS = (
        LivingBeingComponent,
        AnimalComponent,
    )

    def process(self, world):
        # store initial animal list to avoid babys. This will also help us for partner finding
        self.animals = list(Query(component_types=self.COMPONENTS, world=world))
        for entity, components in self.animals:
            self.process_entity(entity, components, world)

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        living_being_cmp.hp += const.ANIMAL_DAILY_REGENERATION

        if living_being_cmp.hp > const.ANIMAL_HUNGER_THRESHOLD:
            # no need to feed today, let find a partner to make a baby
            # first, let’s try to find a partner
            partners = [
                (it_entity, it_components)
                for it_entity, it_components in self.animals
                if it_entity != entity
            ]
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
        # animals gain 3 HP by eating;
        components[0].hp += const.PHYTOPHAGE_RECOVERY_AFTER_EATING
        # plant loose 2 HP when eaten
        target_components[0].hp -= const.PLANT_LIFE_LOST_FROM_ATTACK
