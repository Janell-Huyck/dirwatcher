#! usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Janell.Huyck"

import sys
# import os
# import time

# Make sure that the user is running this program in python3

if sys.version_info[0] < 3:
    raise Exception("This program requires python 3 to work.")
    sys.exit(1)


def main():
    print("main is running")


if __name__ == "__main__":
    main()
