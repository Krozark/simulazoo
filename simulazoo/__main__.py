import argparse
import logging
import sys


from .enclosure import Enclosure, fill_default_enclosure


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


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
