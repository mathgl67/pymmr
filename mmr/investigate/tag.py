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

import mmr
from abstract_investigate import AbstractInvestigate

class Investigate(AbstractInvestigate):
    def _setUp_(self):
        self._album_ = mmr.Album('tag')

    def _do_album_by_tag_name_(self, tag):
        possibilities = dict()

        for f in self._folder_._files_:
            if (f._type_ != "ogg" and f._type_ != "mp3" and
               f._type_ != "flac"):
                continue

        try:
            maybe = getattr(f._extra_data_, tag)
            if possibilities.has_key(maybe):
                possibilities[maybe] += 1
            else:
                possibilities[maybe] = 1
        except:
            pass

        max = 0
        prefered = None
        for key, value in possibilities.iteritems():
            if value > max:
                prefered = key
                max = value

        setattr(self._album_, tag, prefered)

    def _do_album_(self):
        for key in self._album_.__keys__:
            self._do_album_by_tag_name_(key)
        return self._album_