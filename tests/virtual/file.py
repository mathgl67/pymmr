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

import random
import os

from mmr.file import BaseFile 

def generate_name():
    name = ""
    for i in range(0, 20):
        num = random.randrange(97,122)
        name = name + chr(num) 

    return name


def create_file(name=None, path=None):
    if not name:
        name = generate_name()
    if not path:
        path = generate_name()

    return BaseFile.factory(os.path.join(path, name))

def create_file_list(name=None, path=None, number=None):
    list = []

    if not name:
        name = generate_name()
    if not path:
        path = generate_name()
    if not number:
        number = 10

    for i in range(number):
        f = create_file(name + '_' + str(i), path)
        list.append(f)

    return list
