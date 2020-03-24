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
        """Check if parser can parse args"""
        p = dirwatcher.create_parser()
        test_args = ['watchdir', 'txt', '-poll 3', 'Tiffany']
        ns = p.parse_args(test_args)
        self.assertTrue(ns.dir == 'watchdir')
        self.assertTrue(ns.ext == 'txt')
        self.assertTrue(ns.poll == '3')
        self.assertTrue(ns.magic == "Tiffany")
