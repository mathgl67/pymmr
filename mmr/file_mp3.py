#!/usr/bin/env python
# vi:ai:et:ts=2 sw=2
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

from mutagen.mp3 import MP3

class FileMp3:
  def __init__(self, file):
    self.__file__ = file
    self._artist_ = None
    self._title_ = None
    self._year_ = None
    self._genre_ = None
    self._track_ = None
    self._number_ = None

    self.__parse_tags__()  

  def __str__(self):
    str  = "_artist_='%s' " % self._artist_
    str += "_title_='%s' " % self._title_
    str += "_year_='%s' " % self._year_
    str += "_genre_='%s' " % self._genre_
    str += "_track_='%s' " % self._track_
    str += "_number_='%s' " % self._number_
    return str

  def __parse_tags__(self):
    tags = MP3(self.__file__._fullpath_)
    if tags.has_key('artist'):
      self._artist_ = str(tags.get('artist'))
    if tags.has_key('album'):
      self._title_ = str(tags.get('album'))
    if tags.has_key('date'):
      self._year_ = str(tags.get('year'))
    if tags.has_key('genre'):
      self._genre_ = str(tags.get('genre'))
    if tags.has_key('title'):
      self._track_ = str(tags.get('title'))
    if tags.has_key('tracknumber'):
      self._number_ = str(tags.get('tracknumber'))

