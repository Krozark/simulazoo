import argparse
import logging
import sys

from .components import AnimalComponent, PlantComponent, SexEnum
from .enclosure import Enclosure

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


def build_enclosure():
    enclosure = Enclosure("first enclosure")
    # create 3 plants
    enclosure.create_entity(PlantComponent())
    enclosure.create_entity(PlantComponent())
    enclosure.create_entity(PlantComponent())
    # create 2 animals
    enclosure.create_entity(AnimalComponent(name="Alice", sex=SexEnum.FEMALE))
    enclosure.create_entity(AnimalComponent(name="Bob", sex=SexEnum.MALE))
    return enclosure


def main():
    # create an argument parser
    parser = argparse.ArgumentParser(prog="Simulazoo", description="A zoo simulator")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parse the arguments
    args = parser.parse_args()

    setup_logging(verbose=args.verbose)
    enclosure = build_enclosure()
    enclosure.process_day()
    return 0


sys.exit(main())
