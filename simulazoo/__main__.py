import argparse
import logging
import sys

from .components import (
    AnimalComponent,
    LivingBeingComponent,
    PhytophageComponent,
    PlantComponent,
    ZoophageComponent,
)
from .enclosure import Enclosure
from .enums import SexEnum
from .config import parse_config_file


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


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


def fill_enclosure_from_config(file, enclosure):
    for entity_components in parse_config_file(file):
        enclosure.create_entity(
            *[
                component_class(**components_kwargs)
                for component_class, components_kwargs in entity_components.items()
            ]
        )


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def main():
    # create an argument parser
    parser = argparse.ArgumentParser(prog="Simulazoo", description="A zoo simulator")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-d", "--days", type=check_positive, default=1)
    parser.add_argument("-o", "--output", type=argparse.FileType("w"))
    parser.add_argument("-c", "--config", type=argparse.FileType("r"))
    # parse the arguments
    args = parser.parse_args()
    # setup logging
    setup_logging(verbose=args.verbose)
    # create enclosure
    enclosure = Enclosure("first enclosure")

    if args.config:
        logger.info("Load config file, and fill enclosure with informations")
        fill_enclosure_from_config(args.config, enclosure)
    else:
        logger.info("Fill enclosure with default")
        fill_default_enclosure(enclosure)

    # simulate days
    enclosure.log_report()
    for day in range(0, args.days):
        enclosure.process_day()

    # build output file
    if args.output:
        enclosure.save_to_file(args.output)
    return 0


sys.exit(main())
