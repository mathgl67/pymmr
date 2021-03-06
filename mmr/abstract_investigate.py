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

class AbstractInvestigate:
    def __init__(self, folder, album_list, config, base_score):
        self._config_ = config
        self._folder_ = folder
        self._album_list_ = album_list
        self._base_score_ = base_score
        self._album_ = None
        self._tracks_ = {}
        self._set_up_()

    def _set_up_(self):
        pass

    def do_album(self):
        pass

    def do_track(self, file_obj, result_array):
        pass
