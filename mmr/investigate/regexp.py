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

import re

class Investigate(AbstractInvestigate):
    def _setUp_(self):
        self._album_ = mmr.Album('regexp')

    def _do_album_(self):
        regexs = {
            "artist album year":"^([\\d\\w_\ ]+)-([\\d\\w_\ ]+).+([\\d]{4})",
            "artist album":"^([\\d\\w_\ ]+)-([\\d\\w_\ ]+)$",
            "artist album": "^([\\d\\w_\ \'\.]+)\ -\ ([\\d\\w_\ \'\.]+)$",
            "album":"^([\\d\\w_\ ]+)$"
        }

        for keys, regex in regexs.iteritems():
            p = re.compile(regex)
            m = p.match(self._folder_._name_)
            if m:
                i=1
                for attr in keys.split(' '):
                    setattr(self._album_, attr, m.group(i).replace('_', ' '))
                    i+=1

        return self._album_
