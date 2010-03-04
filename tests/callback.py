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

import unittest

from mmr.callback import Callback

# this is needed for callback1 function
passed = { "call": False, "arguments": False }

def callback1(obj, arg):
    global passed
    passed["call"] = True
    if obj == 2222 and arg == 4444: 
        passed["arguments"] = True

class TestCallback(unittest.TestCase):
    @staticmethod
    def suite():
        return unittest.TestSuite([
          unittest.TestLoader().loadTestsFromTestCase(TestCallbackConstructor),
          unittest.TestLoader().loadTestsFromTestCase(TestCallbackCall),
        ])

class TestCallbackConstructor(TestCallback):
    def setUp(self):
        self.callback1 = Callback(callback1, 2222)

    def testConstructorSetFunction(self):
        self.assertEquals(self.callback1.function, callback1)

    def testConstructorSetArgument(self):
        self.assertEquals(self.callback1.object, 2222)

class TestCallbackCall(TestCallback):
    def setUp(self):
        self.callback1 = Callback(callback1, 2222)
        self.callback1(4444)

    def testCallFunction(self):
        global passed
        self.assertTrue(passed["call"])

    def testCallArguments(self):
        global passed
        self.assertTrue(passed["arguments"])

