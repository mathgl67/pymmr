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

"""This file contain the registry class"""

class Registry(object):
    """This class create a registry that will be used to avoid more than
    one class to be a signleton
    """

    _instance = None
    _initialized = False
    def __new__(cls, *args, **kargs):
        """Replace the new class function to act as singleton"""
        if not cls._instance:
            cls._instance = super(Registry, cls).__new__(
                cls, *args, **kargs)
        return cls._instance

    def __init__(self):
        if not Registry._initialized:
            self.clear()
            Registry._initialized = True
   
    def clear(self):
        self.contents = {} 

