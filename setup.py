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

import os
from distutils.core import setup

setup(
    name="mmr",
    version="0.1-alpha0",
    description="My Mysic Renamer",
    author="MathGl",
    author_email="mathgl67@gmail.com",
    url="http://gitorious.com/pymmr",
    packages=[
        "mmr",
        os.path.join("mmr", "investigate"),
        os.path.join("mmr", "curses"),
        os.path.join("mmr", "gtk"),
        os.path.join("mmr", "tags")
    ],
    scripts=["gmmr", "pymmr", "cmmr"]
)

