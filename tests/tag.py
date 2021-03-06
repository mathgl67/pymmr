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

import mmr.file

from mmr.tags.mp3 import Mp3
from mmr.tags.ogg import Ogg
from mmr.tags.flac import Flac

class TestTagMp3(unittest.TestCase):
    def setUp(self):
        self.tag = Mp3(mmr.file.factory('tests/data/tags/silence.mp3'))

    def testArtist(self):
        self.assertEquals(self.tag.artist, u'artist')

    def testAlbum(self):
        self.assertEquals(self.tag.album, u'album')

    def testTitle(self):
        self.assertEquals(self.tag.title, u'title')

    def testDate(self):
        self.assertEquals(self.tag.year, u'2000')

    def testGenre(self):
        self.assertEquals(self.tag.genre, u'genre')

    def testTrackNumber(self):
        self.assertEquals(self.tag.tracknumber, u'1')

class TestTagFlac(TestTagMp3):
    def setUp(self):
        self.tag = Flac(mmr.file.factory('tests/data/tags/silence.flac'))

class TestTagOgg(TestTagMp3):
    def setUp(self):
        self.tag = Ogg(mmr.file.factory('tests/data/tags/silence.ogg'))
