#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Janell.Huyck"

import sys
import argparse
# import os
import datetime
import logging

# Make sure that the user is running this program in python3

if sys.version_info[0] < 3:
    raise Exception("This program requires python 3 to work.")
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger.setLevel(logging.DEBUG)


def create_parser():
    """ Create and return a parser object """

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory to watch')
    parser.add_argument('ext', help="""File extension for type of
                        file to watch in the directory""")
    parser.add_argument('magic', help='The string we are watching for.')
    parser.add_argument('-poll', default="1", help="""How often (in seconds) to
                        poll the directory.  Default is 1 second.""")

    return parser


def main(args):
    app_start_time = datetime.datetime.now()
    logger.info('\n'
                '=========================================================\n'
                '\tRunning {}\n'
                '\tStarted at: {}\n'
                '=========================================================\n'
                .format(__file__, str(app_start_time)))
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    logger.debug("main is running")
    uptime = datetime.datetime.now() - app_start_time
    logger.info('\n'
                '=========================================================\n'
                '\tStopped {}\n'
                '\tUptime was: {}\n'
                '=========================================================\n'
                .format(__file__, str(uptime)))


if __name__ == "__main__":
    main(sys.argv[1:])
