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
import virtual.folder

from mmr.investigate_album import InvestigateAlbum

class TestInvestigateAlbum(unittest.TestCase):
    @staticmethod
    def suite():
        return unittest.TestSuite([
          unittest.TestLoader().loadTestsFromTestCase(TestInvestigateAlbumConstructor),
        ])

class TestInvestigateAlbumConstructor(TestInvestigateAlbum):
    def setUp(self):
        self.folder1 = virtual.folder.create_folder1()
        self.inst1 = InvestigateAlbum(self.folder1)
     

    def testConstructorSetUpFolder(self):
        self.assertEquals(self.inst1.folder, self.folder1)

    def testConstructorSetUpResultList(self):
        self.assertEquals(len(self.inst1.result_list), 0)



