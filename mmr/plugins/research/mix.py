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

from mmr.plugin import AbstractResearchPlugin
from mmr.album import Album
from mmr.track import Track
from mmr.abstract_investigate import AbstractInvestigate

class Mix(AbstractResearchPlugin):
    def setup(self):
        self.investigate_class = MixInvestigate
        self.about = {
            "name": u"Mix",
            "short_description": u"",
            "long_description": u"",
        }
        self.priority = 20

plugin_class=Mix

class MixInvestigate(AbstractInvestigate):
    def _set_up_(self):
        self._album_ = Album('mix', self._base_score_)

    def do_album(self):
        for res in self._album_list_:
            for key in self._album_.get_keys():
                if not getattr(self._album_, key):
                    setattr(self._album_, key, getattr(res, key))
        return self._album_

    def do_track(self, file_obj, result_array):
        track = Track('mix', self._base_score_)
        for result in result_array:
            for key in track.get_keys():
                if not getattr(track, key):
                    setattr(track, key, getattr(result, key))
        return track
