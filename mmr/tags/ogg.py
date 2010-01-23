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


from mmr.tags.abstract_tag import AbstractTag
# Display a fatal error when mutagen is not installed.
# Yaml is require to parse the config file.
try:
    import mutagen.oggvorbis
except ImportError as exception:
    print "FATAL: Mutagen python module is require and must be installed. (python-mutagen)"
    import sys
    sys.exit(1)

class Ogg(AbstractTag):
    def _set_up_(self):
        self._mutagen_ = mutagen.oggvorbis.OggVorbis(self._file_.get_fullpath())
