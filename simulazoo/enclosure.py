import logging

from snecs import Query, World, new_entity

from .components import AnimalComponent, PlantComponent

logger = logging.getLogger(__name__)


class Enclosure:
    def __init__(self, name=None):
        self.world = World(name)
        self._day = 0

    def create_entity(self, *components):
        entity = new_entity(components=components, world=self.world)
        return entity

    def process_day(self):
        for system in self.get_systems():
            system.process()
        self._day += 1
        report = self.build_report()
        logger.info("\n" + report)

    def build_report(self):
        report = [f"==== Report of enclosure {self.world.name}: day {self._day} ==="]
        # start of report

        # stuff with plants
        plant_query = Query([PlantComponent], world=self.world)
        plant_number = sum(1 for _ in plant_query)
        report.append(f"Plant number: {plant_number}")

        # stuff with animals
        animal_query = Query([AnimalComponent], world=self.world)
        report.append("Animals: ")
        for entity, (animal_component,) in animal_query:
            report.append(
                f" - Name: {animal_component.name}, Sex: {animal_component.sex.name}"
            )

        # end of report
        report.append("==============================")
        return "\n".join(report)

    @staticmethod
    def get_systems():
        return ()
