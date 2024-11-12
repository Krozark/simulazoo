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


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


def build_enclosure():
    enclosure = Enclosure("first enclosure")
    # create 3 plants
    for i in range(0, 3):
        enclosure.create_entity(
            LivingBeingComponent("Fern"),
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
    return enclosure


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
    # parse the arguments
    args = parser.parse_args()
    # setup logging
    setup_logging(verbose=args.verbose)
    # create enclosure
    enclosure = build_enclosure()
    enclosure.log_report()
    # simulate days
    for day in range(0, args.days):
        enclosure.process_day()
    return 0


sys.exit(main())
