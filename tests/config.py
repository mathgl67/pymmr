#!/usr/bin/env python
# vi:ai:et:ts=4 sw=4
#
# -*- coding: utf8 -*-
#
# PyMmr My Music Renamer
# Copyright (C) 2007-2010  mathgl67@gmail.com
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import unittest
import tempfile
import os

from mmr.config import Config

class TestConfig(unittest.TestCase):
    def testWithoutArgument(self):
        config = Config({})
        self.assertFalse(config.has_key('test_key'))

    def testWithArguments(self):
        config = Config({ 'test_key1': True, 'test_key2': False })
        self.assertTrue(config.has_key('test_key1'))
        self.assertTrue(config.has_key('test_key2'))
        self.assertTrue(config['test_key1'])
        self.assertFalse(config['test_key2'])

    def testSetValue(self):
        config = Config({ 'test_key1': True })
        config["test_key1"] = False
        self.assertFalse(config["test_key1"])

    def testSaveAndLoad(self):
        # setup a base config file
        config_reader = Config({})
        config_writer = Config({ "test_key1": True, "test_key2": False })
        # open a tempory file
        fd, file_path = tempfile.mkstemp()
        os.close(fd) # not needed
        # save to file
        config_writer.save(file_path)
        # load from file
        config_reader.load(file_path)
        # compare
        self.assertTrue(config_reader["test_key1"])
        self.assertFalse(config_reader["test_key2"])
        # delete it
        os.unlink(file_path)
        
