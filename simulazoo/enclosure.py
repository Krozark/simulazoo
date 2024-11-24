import json
import logging

from snecs import (
    Query,
    World,
    deserialize_world,
    new_entity,
    process_pending_deletions,
    serialize_world
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

from .report import EnclosureReportBuilder

logger = logging.getLogger(__name__)

__all__ = [
    "Enclosure",
    "fill_default_enclosure",
]


class Enclosure:
    """
    This class hold all data from the ECS together.
    It also offers save, load and report capabilities.
    """

    def __init__(self, name=None):
        """
        Create a new Enclosure

        :param name: The name of the enclosure
        """
        self.world = World(name)
        self.day = 0
        self._systems = self._get_systems()

    @property
    def name(self):
        return self.world.name

    def create_entity(self, *components):
        """
        Add a new entity to the enclosure with its components.

        :param components:  Components to add to the entity
        :return: the newly created entity id
        """
        entity = new_entity(components=components, world=self.world)
        return entity

    def process_day(self, log_report: bool=True):
        """
        Loop through all the systems and build a report

        :param log_report: generate the report
        :return: None
        """
        for system in self._systems:
            system.process(world=self.world)
        process_pending_deletions(world=self.world)
        self.day += 1
        if log_report:
            self.log_report()

    def build_report(self) -> str:
        """
        Build a report from the

        :return: The report as a str.
        """
        report_builder = EnclosureReportBuilder(self)
        output = report_builder.build_repport()
        return output.read()

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
    def _get_systems():
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
