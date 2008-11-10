#!/usr/bin/env python
# vi:ai:et:ts=2 sw=2
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

from mmr.tags.mp3 import Mp3
from mmr.tags.ogg import Ogg
from mmr.tags.flac import Flac

class Tag:
    @staticmethod
    def get(file_obj):
        file_type = file_obj.get_type()
        if file_type == 'mp3':
            return Mp3(file_obj)
        if file_type == 'ogg':
            return Ogg(file_obj)
        elif file_type == 'flac':
            return Flac(file_obj)
        return None
