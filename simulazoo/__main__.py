import sys
import logging
import argparse

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


def main():
    # create an argument parser
    parser = argparse.ArgumentParser(prog='Simulazoo',description='A zoo simulator')
    parser.add_argument('-v', '--verbose', action='store_true')
    # parse the arguments
    args = parser.parse_args()

    setup_logging(verbose=args.verbose)
    return 0

sys.exit(main())