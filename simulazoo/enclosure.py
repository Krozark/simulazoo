import logging
import json
from snecs import (
    Query,
    World,
    new_entity,
    process_pending_deletions,
    serialize_world,
    deserialize_world,
)
from snecs.ecs import move_world

from .components import AnimalComponent, LivingBeingComponent, PlantComponent
from .systems import (
    AnimalSystem,
    LivingBeingSystem,
    PhytophageSystem,
    PlantSystem,
    ZoophageSystem,
)
from .config import parse_config_file

logger = logging.getLogger(__name__)

__all__ = [
    "Enclosure",
]


class Enclosure:

    def __init__(self, name=None):
        self.world = World(name)
        self._day = 0
        self._systems = self.get_systems()

    def create_entity(self, *components):
        entity = new_entity(components=components, world=self.world)
        return entity

    def process_day(self):
        for system in self._systems:
            system.process(world=self.world)
        process_pending_deletions(world=self.world)
        self._day += 1
        self.log_report()

    def log_report(self):
        report = [f"==== Report of enclosure {self.world.name}: day {self._day} ==="]
        # start of report

        # stuff with plants
        plant_query = Query([LivingBeingComponent, PlantComponent], world=self.world)
        plant_number = sum(1 for _ in plant_query)
        report.append(f"Plant ({plant_number}):")
        for entity, (
            living_being_cmp,
            animal_cmp,
        ) in plant_query:
            report.append(
                f" - Specie: {living_being_cmp.specie}, HP {living_being_cmp.hp}, Age {living_being_cmp.age}"
            )

        # stuff with animals
        animal_query = Query([LivingBeingComponent, AnimalComponent], world=self.world)
        animal_number = sum(1 for _ in animal_query)
        report.append(f"Animals ({animal_number}): ")
        for entity, (
            living_being_cmp,
            animal_cmp,
        ) in animal_query:
            report.append(
                f" - Name: {animal_cmp.name}, Sex: {animal_cmp.sex.name}, Specie: {living_being_cmp.specie}, HP {living_being_cmp.hp}, Age {living_being_cmp.age}"
            )

        # end of report
        report.append("==============================")
        logger.info("\n" + "\n".join(report))

    def save_to_file(self, file):
        serialized = serialize_world(self.world)
        json.dump(serialized, file)

    def load_from_file(self, file):
        serialized = json.load(file)
        new_world = deserialize_world(serialized)
        move_world(new_world, self.world)

    def load_from_config_file(self, file):
        logger.info("Load config file")
        for entity_components in parse_config_file(file):
            self.create_entity(
                *[
                    component_class(**components_kwargs)
                    for component_class, components_kwargs in entity_components.items()
                ]
            )

    @staticmethod
    def get_systems():
        return (
            # manage need of food
            PlantSystem(),
            AnimalSystem(),
            # manage eat
            PhytophageSystem(),
            ZoophageSystem(),
            # manage death
            LivingBeingSystem(),
        )
