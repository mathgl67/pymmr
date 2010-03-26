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

from mmr.album import Album
from mmr.track import Track
from mmr.investigate.abstract_investigate import AbstractInvestigate
from mmr.file import AudioFile 

class Investigate(AbstractInvestigate):
    def _set_up_(self):
        self._album_ = Album('tag', self._base_score_)

    def _do_album_by_tag_name_(self, tag):
        possibilities = dict()

        for file_obj in self._folder_.file_list:
            if (file_obj.extension != ".ogg" and

                file_obj.extension != ".mp3" and
                file_obj.extension != ".flac"):
                continue

            try:
                maybe = getattr(file_obj.tags, tag)
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

    def do_track(self, file_obj, result_array):
        if not isinstance(file_obj, AudioFile): 
            return None

        track = Track('tag', self._base_score_)
        tags = file_obj.tags

        if tags.tracknumber:
            track.tracknumber = tags.tracknumber
        if tags.title:
            track.title = tags.title

        return track
