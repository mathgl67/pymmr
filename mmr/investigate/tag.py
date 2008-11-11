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
from mmr.track import Track
from mmr.investigate.abstract_investigate import AbstractInvestigate

class Investigate(AbstractInvestigate):
    def _set_up_(self):
        self._album_ = Album('tag')
        self._track_ = Track('tag')

    def _do_album_by_tag_name_(self, tag):
        possibilities = dict()

        for file_obj in self._folder_.get_files():
            if (file_obj.get_type() != "ogg" and
                file_obj.get_type() != "mp3" and
                file_obj.get_type() != "flac"):
                continue

            try:
                maybe = getattr(file_obj.get_tags(), tag)
                if possibilities.has_key(maybe):
                    possibilities[maybe] += 1
                else:
                    possibilities[maybe] = 1
            except:
                pass

        max_value = 0
        prefered = None
        for key, value in possibilities.iteritems():
            if value > max_value:
                prefered = key
                max_value = value

        setattr(self._album_, tag, prefered)

    def do_album(self):
        for key in self._album_.get_keys():
            self._do_album_by_tag_name_(key)
        return self._album_

    def do_track(self, file_obj):
        return self._track_