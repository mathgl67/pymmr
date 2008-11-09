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

class Album:
  def __init__(self, by):
    self.__by__ = by
    self.__score__ = 0
    self.__keys__ = ('artist', 'album', 'genre', 'date')

    self.artist = None
    self.album = None
    self.genre = None
    self.date = None

  def __cmp__(self, other):
    if self.__score__ < other.__score__:
      return 1
    elif self.__score__ > other.__score__:
      return -1
    else:
      return 0

  def __str__(self):
    str = "album by '%s' score '%d' " % (self.__by__, self.__score__)
    for key in self.__keys__:
      str += "%s='%s' " % (key, getattr(self, key))
    return str

  def _calculate_score_(self):
    found = 0
    for key in self.__keys__:
      if getattr(self, key):
        found += 1

    if self.__by__ == 'mix':
      score = 90
    elif self.__by__ == 'tag':
      score = 50
    elif self.__by__ == 'regexp':
      score = 10
    else:
      score = 0

    self.__score__ = score + (found * 100)

