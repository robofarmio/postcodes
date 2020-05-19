import argparse
from pathlib import Path

import postcodes.scripts.extract
import postcodes.scripts.prepare
import postcodes.scripts.pyramid


def main():
    parser = argparse.ArgumentParser(prog="postcodes")

    subcmd = parser.add_subparsers(dest="command")
    subcmd.required = True

    Formatter = argparse.ArgumentDefaultsHelpFormatter

    extract = subcmd.add_parser("extract", help="extracts post codes from OpenStreetMap", formatter_class=Formatter)
    extract.add_argument("out", type=Path, help="path to .geojson out file")
    extract.add_argument("osm", type=Path, help="path to .osm.pbf base map")
    extract.set_defaults(main=postcodes.scripts.extract.main)

    prepare = subcmd.add_parser("prepare", help="prepares post code areas for lookup", formatter_class=Formatter)
    prepare.add_argument("out", type=Path, help="path to .geojson post codes bounds out file")
    prepare.add_argument("postcodes", type=Path, help="path to .geojson post codes file")
    prepare.set_defaults(main=postcodes.scripts.prepare.main)

    pyramid = subcmd.add_parser("pyramid", help="builds post codes prefix search tree", formatter_class=Formatter)
    pyramid.add_argument("out", type=Path, help="path to .geojson pyramid out file")
    pyramid.add_argument("boxes", type=Path, help="path to .geojson post codes boxes file")
    pyramid.set_defaults(main=postcodes.scripts.pyramid.main)

    args = parser.parse_args()
    args.main(args)


if __name__ == "__main__":
    main()
