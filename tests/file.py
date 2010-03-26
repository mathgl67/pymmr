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
from mmr.file import BaseFile, AudioFile

class TestFile(unittest.TestCase):
    @staticmethod
    def suite():
        return unittest.TestSuite([
          unittest.TestLoader().loadTestsFromTestCase(TestFileFactory),
          unittest.TestLoader().loadTestsFromTestCase(TestFileUnknown),
          unittest.TestLoader().loadTestsFromTestCase(TestFileAudio),
        ])

class TestFileFactory(TestFile):
    def setUp(self):
        # create cross os compatible path
        self.file_name = "name.ext"
        self.file_path = os.path.join("tests", "data", "file")
        self.file_fullpath = os.path.join(
            self.file_path,
            self.file_name
        ) 
        # create a base file object with previous data
        # this will be used for all test in this class.
        self.file = BaseFile.factory(self.file_fullpath)

    def testName(self):
        self.assertEquals(
            self.file.name, self.file_name,
            "Factory must set the name to '%s' and it was '%s' !" % (
                self.file_name,
                self.file.name
            )
        )

    def testExtension(self):
        self.assertEquals(
            self.file.extension, ".ext",
            "Factory must set extension to '%s' and it was '%s' !" % (
                ".ext",
                self.file.extension
            )
        )

    def testPath(self):
        self.assertEquals(
            self.file.path, self.file_path,
            "Factory must set path to '%s' and it was '%s' !" % (
                self.file_path,
                self.file.path
              )
        )

    def testFullpath(self):
        self.assertEquals(
            self.file.get_fullpath(), self.file_fullpath,
            "Factory must retrieve path to '%s' (!= '%s')." % (
                self.file_fullpath,
                self.file.get_fullpath()
            )
        )


class TestFileUnknown(TestFile):
    def setUp(self):
        self.file = BaseFile.factory("tests/data/file/unknown")

    def testObjectType(self):
        self.assertTrue(isinstance(self.file, BaseFile), "file should be a BaseFile object")

    def testExtention(self):
        self.assertEquals(self.file.extension, None, "file extension on unknown file should be None != %s" % self.file.extension)

class TestFileAudio(TestFile):
    def setUp(self):
        self.file = {
          ".mp3": BaseFile.factory("tests/data/tags/silence.mp3"),
          ".ogg": BaseFile.factory("tests/data/tags/silence.ogg"),
          ".flac":BaseFile.factory("tests/data/tags/silence.flac"),
        }

    def testMp3FileIsFileAudio(self):
        self.assertTrue(isinstance(self.file[".mp3"], AudioFile), "File with '.mp3' extension should be 'AudioFile'")

    def testOggFileIsFileAudio(self):
        self.assertTrue(isinstance(self.file[".ogg"], AudioFile), "File with '.ogg' extension should be 'AudioFile'")

    def testFlacFileIsFileAudio(self):
        self.assertTrue(isinstance(self.file[".flac"], AudioFile), "File with '.flac' extension should be 'AudioFile'")

    def testHaveTag(self):
        self.assertNotEquals(self.file[".mp3"].tags, None)
        self.assertNotEquals(self.file[".ogg"].tags, None)
        self.assertNotEquals(self.file[".flac"].tags, None)
