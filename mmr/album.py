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

"""This file contain the Album class"""

from mmr.config import Config

class Album:
    """This represent an Album"""

    def __init__(self, investigater):
        """Constructor: initialize data

          investigater -- the module who provide data
        """
        self._investigater_ = investigater
        self._score_ = 0
        self._keys_ = ('artist', 'album', 'genre', 'year')

        # set all keys to None
        for key in self._keys_:
            setattr(self, key, None)

    def __cmp__(self, other):
        """Compare two object by score"""
        if self._score_ < other.get_score():
            return 1
        elif self._score_ > other.get_score():
            return -1
        else:
            return 0

    def __repr__(self):
        """Return a representation of this object"""
        lines = []
        lines.append(u"<album investigater=\"%s\" score=\"%d\">" % (
                     self._investigater_, self._score_))

        for key in self.get_keys():
            lines.append(u"<%s>%s</%s>" % (key, getattr(self, key), key))

        lines.append(u"</album>")
        return u"\n".join(lines)

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

    def get_score(self):
        """Return the score"""
        return self._score_

    def get_keys(self):
        """Return keys"""
        return self._keys_
