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
from mmr.file import File, FileAudio

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
        self.file = File.factory("tests/data/file/name.ext")

    def testName(self):
        self.assertEquals(self.file.name, "name.ext", "Factory must set the name to 'name' and it was '%s' !" % self.file.name)

    def testExtension(self):
        self.assertEquals(self.file.extension, ".ext", "Factory must set extension to 'ext' and it was '%s' !" % self.file.extension)

    def testPath(self):
        self.assertEquals(self.file.path, "tests/data/file", "Factory must set path to 'tests/data/file/name.ext' ans it was '%s' !" % self.file.path )

    def testFullpath(self):
        self.assertEquals(self.file.get_fullpath(), "tests/data/file/name.ext")


class TestFileUnknown(TestFile):
    def setUp(self):
        self.file = File.factory("tests/data/file/unknown")

    def testObjectType(self):
        self.assertTrue(isinstance(self.file, File), "file should be a File object")

    def testExtention(self):
        self.assertEquals(self.file.extension, None, "file extension on unknown file should be None != %s" % self.file.extension)

class TestFileAudio(TestFile):
    def setUp(self):
        self.file = {
          ".mp3": File.factory("tests/data/tags/silence.mp3"),
          ".ogg": File.factory("tests/data/tags/silence.ogg"),
          ".flac": File.factory("tests/data/tags/silence.flac"),
        }

    def testMp3FileIsFileAudio(self):
        self.assertTrue(isinstance(self.file[".mp3"], FileAudio), "File with '.mp3' extension should be 'FileAudio'")

    def testOggFileIsFileAudio(self):
        self.assertTrue(isinstance(self.file[".ogg"], FileAudio), "File with '.ogg' extension should be 'FileAudio'")

    def testFlacFileIsFileAudio(self):
        self.assertTrue(isinstance(self.file[".flac"], FileAudio), "File with '.flac' extension should be 'FileAudio'")

    def testHaveTag(self):
        self.assertNotEquals(self.file[".mp3"].tags, None)
        self.assertNotEquals(self.file[".ogg"].tags, None)
        self.assertNotEquals(self.file[".flac"].tags, None)
