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

import re
from album import Album

class InvestigateAlbum:
  def __init__(self, folder):
    self.__folder__ = folder
    self.__results__ = list()

  def __str__(self):
    str = "InvestigateAlbum results:"
    for res in self.__results__:
      str += "\n" + res.__str__()
    return str

  def _append_(self, album):
    album._calculate_score_()
    self.__results__.append(album)

  def count(self, album):
    return len(self.__results__)

  def get_album(self, num):
    return self.__results__[num]

  def sort(self):
    self.__results__.sort()

  def do_by_regex(self):
    album = Album("regexp")
    regexs = {
      "_artist_ _title_ _year_":"^([\\d\\w_\ ]+)-([\\d\\w_\ ]+).+([\\d]{4})",
      "_artist_ _title_":"^([\\d\\w_\ ]+)-([\\d\\w_\ ]+)$",
      "_title_":"^([\\d\\w_\ ]+)$"
    }

    for keys, regex in regexs.iteritems():
      p = re.compile(regex)
      m = p.match(self.__folder__._name_)
      if m:
        i=1
        for attr in keys.split(' '):
          setattr(album, attr, m.group(i))
          i+=1
    
    self._append_(album)
  
  def __do_by_tag_name__(self, album, tag):
    possibilities = dict()

    for f in self.__folder__._files_:
      if (f._type_ != "ogg") and (f._type_ != "mp3") and (f._type_ != "flac"):
        continue

      maybe = getattr(f._extra_data_, tag)
      if possibilities.has_key(maybe):
        possibilities[maybe] += 1
      else:
        possibilities[maybe] = 1

    max = 0
    prefered = None
    for key, value in possibilities.iteritems():
      if value > max:
        prefered = key
        max = value
    
    setattr(album, tag, prefered)


  def do_by_tag(self):
    album = Album("tag")
    for key in album.__keys__:
      self.__do_by_tag_name__(album, key)
    self._append_(album) 
    
  def do_by_mix(self):
    album = Album("mix")
    for res in self.__results__:
      for key in album.__keys__:
        if not getattr(album, key):
          setattr(album, key, getattr(res, key))
    self._append_(album)

