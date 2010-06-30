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

from mmr.folder import Folder
from mmr.file import factory 

def create_folder1():
    return Folder(
        "folder1",
        "/somewhere", [
            factory("00-Artist-Album.m3u"),
            factory("00-Artist-Album.nfo"),
            factory("01-title1.mp3"),
            factory("02-title2.mp3"),
            factory("03-title3.mp3"),
            factory("04-title4.mp3"),
        ]
    )

