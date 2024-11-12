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


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def main():
    # create an argument parser
    parser = argparse.ArgumentParser(prog="Simulazoo", description="A zoo simulator")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Activate debug log"
    )
    parser.add_argument(
        "-d",
        "--days",
        type=check_positive,
        default=1,
        help="Number of days to simulate",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        help="Output file to save current state",
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-c",
        "--config",
        type=argparse.FileType("r"),
        help="Load configuration file. Usefull for first run.",
    )
    input_group.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        help="Load file generated with --output",
    )
    # parse the arguments
    args = parser.parse_args()
    # setup logging
    setup_logging(verbose=args.verbose)
    # create enclosure
    enclosure = Enclosure("first enclosure")

    if args.config:
        enclosure.load_from_config_file(args.config)
    elif args.input:
        enclosure.load_from_file(args.input)
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
