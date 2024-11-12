import random

from snecs import Query, entity_component, schedule_for_deletion
from . import const

from .components import (
    AnimalComponent,
    LivingBeingComponent,
    PhytophageComponent,
    PlantComponent,
    ZoophageComponent,
)

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


class AnimalSystem(SystemBase):
    COMPONENTS = (
        LivingBeingComponent,
        AnimalComponent,
    )

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        living_being_cmp.hp += const.ANIMAL_DAILY_REGENERATION

        if living_being_cmp.hp > const.ANIMAL_HUNGER_THRESHOLD:
            # no need to feed today, let find a partner to make a baby
            pass


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
