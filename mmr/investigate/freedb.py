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
from mmr.album import Album
from mmr.track import Track
from mmr.investigate.abstract_investigate import AbstractInvestigate

# Display a fatal error when MySQLdb is not installed.
try:
    import MySQLdb
except ImportError as exception:
    print "FATAL: MySQLdb python module is require and must be installed. (python-mysql)"
    import sys
    sys.exit(1)


class Investigate(AbstractInvestigate):
    def _set_up_(self):
        self.db = MySQLdb.connect(
            host=self._config_['host'],
            user=self._config_['user'],
            passwd=self._config_['password'],
            db=self._config_['db']
        )
        self.db.set_character_set("utf8")
        self._album_ = Album('freedb', self._base_score_)

    def do_album(self):
        for res in self._album_list_:
            if res.artist and res.album:
                artist = res.artist.encode("UTF-8")
                album = res.album.encode("UTF-8")
                self.db.query("""
                    SELECT genre, year FROM album WHERE artist LIKE "%s" AND title LIKE "%s"
                """ % ( artist, album ))
                
                r = self.db.store_result()
                for (genre, year) in r.fetch_row(0):
                    self._album_.artist = res.artist
                    self._album_.album = res.album
                    self._album_.genre = unicode(genre, "UTF-8")
                    self._album_.year = unicode(str(year), "UTF-8")

        return self._album_

    def do_track(self, file_obj, result_array):
        return None

