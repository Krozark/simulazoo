from io import StringIO

from snecs import (
    Query
)

from .components import (
    AnimalComponent,
    LivingBeingComponent,
    PlantComponent,
)

__all__ = [
    "EnclosureReportBuilder",
]

class EnclosureReportBuilder:
    """
    Class that handle report logic for an enclosure
    """
    def __init__(self, enclosure, output = None):
        """
        :param enclosure: Enclosure
        :param output: file like object to write (default is StringIO)
        """
        self.enclosure = enclosure
        self.output = output or StringIO()

    def build_repport(self):
        """
        Write a complet report to the output.

        :return: output
        """
        self._build_header()
        self._build_body()
        self._build_footer()
        self.output.seek(0)
        return self.output

    def _build_header(self):
        self.output.write(f"==== Report of enclosure {self.enclosure.name}: day {self.enclosure.day} ===\n")

    def _build_body(self):
        # stuff with plants
        plant_query = Query([LivingBeingComponent, PlantComponent], world=self.enclosure.world)
        plant_number = sum(1 for _ in plant_query)
        self.output.write(f"Plant ({plant_number}):\n")
        for entity, (
                living_being_cmp,
                animal_cmp,
        ) in plant_query:
            self.output.write(
                f" - Specie: {living_being_cmp.specie}, HP {living_being_cmp.hp}, Age {living_being_cmp.age}\n"
            )

        # stuff with animals
        animal_query = Query([LivingBeingComponent, AnimalComponent], world=self.enclosure.world)
        animal_number = sum(1 for _ in animal_query)
        self.output.write(f"Animals ({animal_number}):\n")
        for entity, (
                living_being_cmp,
                animal_cmp,
        ) in animal_query:
            self.output.write(
                f" - Name: {animal_cmp.name}, Sex: {animal_cmp.sex.name}, Specie: {living_being_cmp.specie}, HP {living_being_cmp.hp}, Age {living_being_cmp.age}\n"
            )

    def _build_footer(self):
        self.output.write("=" * 20)


