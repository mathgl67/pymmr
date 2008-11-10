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

class AbstractTag:
    def __init__(self, file_obj):
        # set default values
        self._file_ = file_obj
        self._data_ = {}
        self._mutagen_ = None
        self._tag_list_ = {
            'artist': 'artist',
            'album': 'album',
            'year': 'year',
            'genre': 'genre',
            'title': 'title',
            'tracknumber': 'tracknumber',
        }
        # do the job
        self._set_up_()
        self._parse_()

    def __repr__(self):
        lines = []
        lines.append('artist=' + self.artist)
        lines.append('album=' + self.album)
        lines.append('title=' + self.title)
        lines.append('year=' + self.year)
        lines.append('genre=' + self.genre)
        lines.append('tracknumber=' + self.tracknumber)
        return "\n".join(lines)

    def __getattr__(self, name):
        if self._data_.has_key(name):
            return self._data_[name]
        raise AttributeError, name

    def _set_up_(self):
        pass

    def _parse_(self):
        for key, value in self._tag_list_.items():
            if self._mutagen_.has_key(value):
                bytes = self._mutagen_.get(value)[0]
                self._data_[key] = unicode(bytes)
