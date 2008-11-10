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

from mmr.album import Album
from mmr.investigate.abstract_investigate import AbstractInvestigate

class Investigate(AbstractInvestigate):
    def _set_up_(self):
        self._album_ = Album("mix")

    def _do_album_(self):
        for res in self._album_list_:
            for key in self._album_.__keys__:
                if not getattr(self._album_, key):
                    setattr(self._album_, key, getattr(res, key))
        return self._album_
