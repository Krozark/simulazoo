import logging

from snecs import Query, World, new_entity, process_pending_deletions

from .components import AnimalComponent, LivingBeingComponent, PlantComponent
from .systems import PhytophageSystem, ZoophageSystem

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
        report.append(f"Plant number: {plant_number}")

        # stuff with animals
        animal_query = Query([LivingBeingComponent, AnimalComponent], world=self.world)
        animal_number = sum(1 for _ in animal_query)
        report.append(f"Animals ({animal_number}): ")
        for entity, (
            living_being_cmp,
            animal_cmp,
        ) in animal_query:
            report.append(
                f" - Name: {animal_cmp.name}, Sex: {animal_cmp.sex.name}, Specie: {living_being_cmp.specie}"
            )

        # end of report
        report.append("==============================")
        logger.info("\n" + "\n".join(report))

    @staticmethod
    def get_systems():
        return (
            PhytophageSystem(),
            ZoophageSystem(),
        )
