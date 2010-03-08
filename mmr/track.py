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

from mmr.config import Config

class Track:
    def __init__(self, investigater):
        self._investigater_ = investigater
        self._score_ = None
        self._keys_ = [ 'tracknumber', 'title' ]
        self.tracknumber = None
        self.title = None


    def calculate_score(self):
        """Calc a score for theses entries"""
        found = 0
        for key in self._keys_:
            if getattr(self, key):
                found += 1

        score = Config().values['score']['default']
        for module, base_score in Config().values['score'].items():
            if self._investigater_ == module:
                score = base_score

        self._score_ = score + (found * 100)

    def __repr__(self):
        string  = u'<track investigater="%s" score="%s"'
        string += u' tracknumber="%s" title="%s"/>'

        return string % (
            self._investigater_, self._score_,
            self.tracknumber, self.title
        )

    def get_keys(self):
        return self._keys_
