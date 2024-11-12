import json
import logging

from snecs import (
    Query,
    World,
    deserialize_world,
    new_entity,
    process_pending_deletions,
    serialize_world,
)
from snecs.ecs import move_world

from .components import (
    AnimalComponent,
    LivingBeingComponent,
    PhytophageComponent,
    PlantComponent,
    ZoophageComponent,
)
from .config import parse_config_file
from .enums import SexEnum
from .systems import (
    AnimalSystem,
    LivingBeingSystem,
    PhytophageSystem,
    PlantSystem,
    ZoophageSystem,
)

logger = logging.getLogger(__name__)

__all__ = [
    "Enclosure",
    "fill_default_enclosure",
]


class Enclosure:

    def __init__(self, name=None):
        self.world = World(name)
        self._day = 0
        self._systems = self.get_systems()

    def create_entity(self, *components):
        entity = new_entity(components=components, world=self.world)
        return entity

    def process_day(self, log_report=True):
        for system in self._systems:
            system.process(world=self.world)
        process_pending_deletions(world=self.world)
        self._day += 1
        if log_report:
            self.log_report()

    def build_report(self):
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
        return "\n".join(report)

    def log_report(self):
        report = self.build_report()
        logger.info("\n" + report)

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


def fill_default_enclosure(enclosure):
    # create 3 Fern plants
    for i in range(0, 3):
        enclosure.create_entity(
            LivingBeingComponent("Fern"),
            PlantComponent(),
        )
    # create 1 Oak tree plants
    enclosure.create_entity(
        LivingBeingComponent("Oak tree"),
        PlantComponent(),
    )
    # create some animals
    ## Lion
    enclosure.create_entity(
        LivingBeingComponent("Lion"),
        ZoophageComponent(),
        AnimalComponent(name="Alice", sex=SexEnum.FEMALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Lion"),
        ZoophageComponent(),
        AnimalComponent(name="Bob", sex=SexEnum.MALE),
    )
    ## Tiger
    enclosure.create_entity(
        LivingBeingComponent("Tiger"),
        ZoophageComponent(),
        AnimalComponent(name="Carol", sex=SexEnum.FEMALE),
    )
    ## Coyote
    enclosure.create_entity(
        LivingBeingComponent("Coyote"),
        ZoophageComponent(),
        AnimalComponent(name="Dave", sex=SexEnum.MALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Coyote"),
        ZoophageComponent(),
        AnimalComponent(name="Eve", sex=SexEnum.FEMALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Coyote"),
        ZoophageComponent(),
        AnimalComponent(name="Frank", sex=SexEnum.MALE),
    )
    ## Elephant
    enclosure.create_entity(
        LivingBeingComponent("Elephant"),
        PhytophageComponent(),
        AnimalComponent(name="Grace", sex=SexEnum.FEMALE),
    )
    ## Giraffe
    enclosure.create_entity(
        LivingBeingComponent("Giraffe"),
        PhytophageComponent(),
        AnimalComponent(name="Heidi", sex=SexEnum.FEMALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Giraffe"),
        PhytophageComponent(),
        AnimalComponent(name="Ivan", sex=SexEnum.MALE),
    )
    ## Antelope
    enclosure.create_entity(
        LivingBeingComponent("Antelope"),
        PhytophageComponent(),
        AnimalComponent(name="Judy", sex=SexEnum.FEMALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Antelope"),
        PhytophageComponent(),
        AnimalComponent(name="Kevin", sex=SexEnum.MALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Antelope"),
        PhytophageComponent(),
        AnimalComponent(name="Laura", sex=SexEnum.FEMALE),
    )
    enclosure.create_entity(
        LivingBeingComponent("Antelope"),
        PhytophageComponent(),
        AnimalComponent(name="Mallory", sex=SexEnum.MALE),
    )
