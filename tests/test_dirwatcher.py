#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A Test fixture for dir_watcher.
    Checks the create_parser, and main functions for
    correct behavior.
"""
import sys
import os
import glob
import unittest

import dirwatcher

__author__ = "Janell.Huyck, based off madarp's test code for babynames"


class TestDirwatcher(unittest.TestCase):
    def test_create_parser(self):
        """Check if parser can parse args correctly"""
        p = dirwatcher.create_parser()
        test_args = ['watchdir', 'txt', '-poll', '3', 'Tiffany']
        ns = p.parse_args(test_args)
        self.assertTrue(ns.dir == 'watchdir', 'Incorrectly parsing dir')
        self.assertTrue(ns.ext == 'txt', 'Incorrectly parsing ext')
        self.assertTrue(
            ns.poll == '3', 'Incorrectly parsing given polling time')
        self.assertTrue(ns.magic == 'Tiffany',
                        'Incorrectly parsing magic string')

        """Check if the default polling time comes back as 1"""

        test_args = ['watchdir', 'txt', 'Tiffany']
        ns = p.parse_args(test_args)
        self.assertTrue(
            ns.poll == '1', "Default polling time should be 1 second")

    # def test_exit_sigint():
