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
import os

from mmr.folder import Folder

from tests.virtual.file import * 

class TestFolder(unittest.TestCase):
    @staticmethod
    def suite():
        return unittest.TestSuite([
          unittest.TestLoader().loadTestsFromTestCase(TestFolderFactory),
          unittest.TestLoader().loadTestsFromTestCase(TestFolderConstructor),
          unittest.TestLoader().loadTestsFromTestCase(TestFolderFunctions),
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

class TestFolderConstructor(TestFolder):
    def setUp(self):
        self.folder = Folder("name", "path", ["file1", "file2"])

    def testFieldName(self):
        self.assertEquals(self.folder.name, "name", "Constructor should set name to 'name' and it was '%s'" % (self.folder.name))

    def testFieldPath(self):
        self.assertEquals(self.folder.path, "path", "Constructor should set path to 'path' and it was '%s'" % (self.folder.path))

    def testFiledFileList(self):
        ## @todo change to a real file list..
        self.assertEquals(self.folder.file_list, ["file1", "file2"])

class TestFolderFunctions(TestFolder):
    def setUp(self):
        self.folder = Folder("name", "path")
    
    def testFolderFunctionStr(self):
        self.assertEquals(self.folder.__str__(), "<Folder name='name' path='path'>\n</Folder>")
    
    def testFolderFunctionGetFullpath(self):
        self.assertEquals(self.folder.get_fullpath(), os.path.join("path", "name"))

    def testFolderFunctionRetrieveFileList(self):
        self.folder = Folder("folder", "tests/data")
        self.folder.retrieve_file_list()
        self.assertEquals(len(self.folder.file_list), 1)
        self.assertTrue(isinstance(self.folder.file_list, list))

