#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Janell.Huyck with help on signals from madarp"

import sys
import argparse
import os
import datetime
import logging
import time
import signal


# Global flag that triggers when SIGINT or SIGTERM occurs
exit_flag = False


# We are going to use a dictionary of key=filename,
# value=[Boolean-has-been-announced, last-line-checked]
# filename = "filename"
# announced = False
# last_line = 0
# previous_files = {filename: [announced, last_line]}


# Make sure that the user is running this program in python3
if sys.version_info[0] < 3:
    raise Exception("This program requires python 3 to work.")
    sys.exit(1)


# Create a logger to print date/time stamps for all logged messages
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger.setLevel(logging.DEBUG)


def signal_handler(sig_num, frame):
    """ This handles SIGINT and SIGTERM signals
    sent to the program and also any other signals.  It changes
    a global flag so that the loop in main() will finish."""

    logger.warn(signal.Signals(sig_num).name + " signal received.")
    global exit_flag
    exit_flag = True


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


def check_files(old_file_dict, parsed_args):
    """ Search the current files in the specified directory and
    return a dictionary of them.  Compare old and new dictionaries and
    log a message for every change."""

    new_file_dict = {}

    # check that parsed_args.ext starts with "." and if it
    # doesn't, add a "." at the beginning.
    extension = parsed_args.ext
    if extension[0] != ".":
        extension = "." + extension

    # write all current files that have the extension to new_file_dict
    walked_path = os.walk(parsed_args.dir)
    for dirpath, dirs, files in walked_path:
        for file_name in files:
            f_name, file_extension = os.path.splitext(
                file_name)
            if file_extension != extension:
                continue
            if len(file_name) > 0:
                new_file_dict[os.path.join(dirpath, file_name)] = 0

    # compare new and old dictionaries and look for changes
    for key, value in new_file_dict.items():
        if key not in old_file_dict:
            logger.info("New file found: " + key)
        else:
            new_file_dict[key] = old_file_dict[key]
    for key, value in old_file_dict.items():
        if key not in new_file_dict:
            logger.info("File deleted: " + key)

    return new_file_dict


def look_for_magic(file_dict, magic):
    """ Looks for a 'magic' string inside every file in a given
    dictionary. Logs finding the string exactly once."""

    for key, value in file_dict.items():

        # make a list of all the unread lines in each file
        with open(key) as fp:
            unread_lines = [[i+1, line]
                            for i, line in enumerate(fp) if i >= value]

            # check each unread line for magic string
            if not unread_lines:
                continue
            for unread_line in unread_lines:
                if magic in unread_line[1]:
                    logger.info("Found " + magic + " in line " +
                                str(unread_line[0]) + " of " + key)

            # set the value of each dictionary item to the last line read
            last_index = unread_lines[-1][0]
            file_dict[key] = last_index

    return file_dict


def poll_directory(parsed_args):
    """ Every polling cycle, check for and report
    changes in the watched directory."""

    old_file_dict = {}
    directory = parsed_args.dir

    # exit_flag is an exit flag triggered by SIGINT and SIGTERM
    while not exit_flag:

        # if the directory to watch doesn't exist, squawk every polling cycle
        if not os.path.isdir(directory):
            logger.info(directory + " is not a directory.")
            time.sleep((int(parsed_args.poll)))
            continue

        # check for new or deleted files
        old_file_dict = check_files(
            old_file_dict, parsed_args)

        # check all current files for magic string
        old_file_dict = look_for_magic(old_file_dict, parsed_args.magic)

        # wait the polling time
        time.sleep(int(parsed_args.poll))


def main(args):
    """ Starts and stops a long-running program watching
    for changes in a specific directory."""

    # Print out a banner at the start of the log indicating start time.
    app_start_time = datetime.datetime.now()
    logger.info('\n'
                '=========================================================\n'
                '\tRunning {}\n'
                '\tStarted at: {}\n'
                '=========================================================\n'
                .format(__file__, str(app_start_time)))

    # Makes it so that keyboard interruptions run signal_handler() and quit.
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Parse the command line arguments
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    parsed_args = parser.parse_args(args)

    # Every polling integer, check for changes in directory and log them.
    poll_directory(parsed_args)

    # After exit_flag = True, gracefully exit program.
    uptime = datetime.datetime.now() - app_start_time
    logger.info('\n'
                '=========================================================\n'
                '\tStopped {}\n'
                '\tUptime was: {}\n'
                '=========================================================\n'
                .format(__file__, str(uptime)))


if __name__ == "__main__":
    main(sys.argv[1:])
