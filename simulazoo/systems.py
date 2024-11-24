import random

from snecs import Query, entity_component, schedule_for_deletion

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


## Bases


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
        if living_being_cmp.hp > 5:
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


## Real systems


class LivingBeingSystem(SystemBase):
    COMPONENTS = (LivingBeingComponent,)

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        if living_being_cmp.hp <= 0:
            schedule_for_deletion(entity, world=world)


class PlantSystem(SystemBase):
    COMPONENTS = (
        LivingBeingComponent,
        PlantComponent,
    )

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        living_being_cmp.hp += 1


class AnimalSystem(SystemBase):
    COMPONENTS = (
        LivingBeingComponent,
        AnimalComponent,
    )

    def process_entity(self, entity, components, world):
        living_being_cmp = components[0]
        living_being_cmp.hp -= 1


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
        # animals gain 5 HP by eating;
        components[0].hp += 5
        # animals loose 4 HP when eaten
        target_components[0].hp -= 4


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
        components[0].hp += 3
        # plant loose 2 HP when eaten
        target_components[0].hp -= 2
