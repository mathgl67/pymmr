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
from mmr.config import Config
from mmr.album import Album
from mmr.track import Track
from mmr.abstract_investigate import AbstractInvestigate

import re

class Regexp(AbstractResearchPlugin):
    def setup(self):
        self.investigate_class = RegexpInvestigate
        self.about = {
            "name": u"Regexp",
            "short_description": u"",
            "long_description": u"",
        }

class RegexpInvestigate(AbstractInvestigate):
    def _set_up_(self):
        self._album_ = Album('regexp', self._base_score_)

    def do_album(self):
        for keys, regex in self._config_['album'].iteritems():
            re_compiled = re.compile(regex)
            match = re_compiled.match(self._folder_.name)
            if match:
                index = 1
                for attr in keys.split(' '):
                    value = match.group(index).replace('_', ' ')
                    setattr(self._album_, attr, value)
                    index += 1

        return self._album_

    def do_track(self, file_obj, result_array):
        self._track_ = Track('regexp', self._base_score_)
        for keys, regex in self._config_['track'].iteritems():
            re_compiled = re.compile(regex)
            match = re_compiled.match(file_obj.name)
            if match:
                index = 1
                for attr in keys.split(' '):
                    value = match.group(index).replace('_', ' ')
                    setattr(self._track_, attr, value)
                    index += 1
        return self._track_
