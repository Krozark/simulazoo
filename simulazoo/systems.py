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
    "ZoophageSystem",
    "PhytophageSystem",
]


class SystemBase:
    COMPONENTS = ()

    def process(self, world):
        for entity, components in Query(component_types=self.COMPONENTS, world=world):
            self.process_entity(entity, components, world)

    def process_entity(self, entity, components, world):
        raise NotImplementedError


class LivingBeingSystem(SystemBase):
    COMPONENTS = (LivingBeingComponent,)

    def process_entity(self, entity, components, world):
        if components[0].hp <= 0:
            schedule_for_deletion(entity, world=world)


class _DietSystem(SystemBase):
    # system that manage diet
    # COMPONENTS eat DIET
    DIET = ()

    def process(self, world):
        self.entity_targeted = {
            entity for entity, _ in Query(component_types=self.DIET, world=world)
        }
        super().process(world)

    def process_entity(self, entity, components, world):
        entity_specie = entity_component(
            entity, LivingBeingComponent, world=world
        ).specie
        # remove same specie as valid choice (this include the current entity)
        invalid_entity = {
            entity
            for entity in self.entity_targeted
            if entity_component(entity, LivingBeingComponent, world=world).specie
            == entity_specie
        }
        # build valid food choice list
        food_choices = self.entity_targeted - invalid_entity
        if food_choices:
            entity_to_delete = random.choice(list(food_choices))
        else:
            # no more food, so the entity die
            entity_to_delete = entity
        schedule_for_deletion(entity_to_delete, world=world)


class ZoophageSystem(_DietSystem):
    # ZoophageComponent eat AnimalComponent
    COMPONENTS = (
        LivingBeingComponent,
        ZoophageComponent,
    )
    DIET = (
        LivingBeingComponent,
        AnimalComponent,
    )


class PhytophageSystem(_DietSystem):
    # PhytophageComponent eat PlantComponent
    COMPONENTS = (
        LivingBeingComponent,
        PhytophageComponent,
    )
    DIET = (
        LivingBeingComponent,
        PlantComponent,
    )
