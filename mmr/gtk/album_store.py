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

import gtk

class AlbumStore(gtk.ListStore):
  def __init__(self):
    super(AlbumStore, self).__init__(str, int, str, str, str, str)
    self._album_list = {}

  def append(self, album):
    iter = super(AlbumStore, self).append([
            album._investigater_,
            album._score_,
            album.artist,
            album.album,
            album.genre,
            album.year
    ])

    iter_path = self.get_string_from_iter(iter)
    self._album_list[iter_path] = album

  def get_album(self, iter):
    iter_path = self.get_string_from_iter(iter)
    return self._album_list[iter_path]

