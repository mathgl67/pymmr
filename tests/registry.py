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
from mmr.registry import Registry

class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        # in test we must keep in mind that the registry can easily
        # be corupt by an other class. So clear is the rules.
        self.registry.clear()

    def testSingleton(self):
        self.registry.clear()
        self.registry.contents['test'] = None 
        other_registry = Registry()
        self.assertTrue(other_registry.contents.has_key('test'))

    def testSetValue(self):
        self.registry.clear()
        self.registry.contents['test'] = None
        self.assertTrue(self.registry.contents.has_key('test'))

    def testGetValue(self):
        self.registry.clear()
        self.registry.contents['test'] = True
        self.assertTrue(self.registry.contents['test'])

