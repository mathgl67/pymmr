#!/usr/bin/env python
# vi:ai:et:ts=4 sw=4
#
# -*- coding: utf8 -*-
#
# PyMmr My Music Renamer
# Copyright (C) 2007  mathgl67@gmail.com
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
from mmr.folder import Folder

class TestFolder(unittest.TestCase):
    @staticmethod
    def suite():
        return unittest.TestSuite([
          unittest.TestLoader().loadTestsFromTestCase(TestFolderFactory),
        ])

class TestFolderFactory(TestFolder):
    def setUp(self):
        self.folder = Folder.factory("tests/data/folder")

    def testInstance(self):
        self.assertTrue(isinstance(self.folder, Folder))

    def testName(self):
        self.assertEquals(self.folder.name, "folder", "Factory must set the name to 'folder' and it was '%s' !" % self.folder.name)

    def testPath(self):
        self.assertEquals(self.folder.path, "tests/data", "Factory must set path to 'tests/data/file/name.ext' ans it was '%s' !" % self.folder.path )

    def testFullpath(self):
        self.assertEquals(self.folder.get_fullpath(), "tests/data/folder")

    def testFileList(self):
        self.assertEquals(len(self.folder.file_list), 1)
        self.assertTrue(isinstance(self.folder.file_list, list))

