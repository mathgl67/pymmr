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

from tag import TestTag
from file import TestFile
from config import TestConfig
from folder import TestFolder
from investigate_album import TestInvestigateAlbum
from callback import TestCallback
from registry import TestRegistry

all_tests = unittest.TestSuite([
  TestFile.suite(),
  TestTag.suite(),
  TestFolder.suite(),
  TestInvestigateAlbum.suite(),
  TestCallback.suite(),
  unittest.TestLoader().loadTestsFromTestCase(TestConfig),
  unittest.TestLoader().loadTestsFromTestCase(TestRegistry),
])

