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

from album import Album
import investigate

class InvestigateAlbum:
  def __init__(self, folder):
    self.__folder__ = folder
    self.__results__ = list()

  def __repr__(self):
    lines = []
    lines.append('<InvestigateAlbum>')
    for res in self.__results__:
      lines.append(repr(res))
    lines.append('</InvestigateAlbum>')
    return "\n".join(lines)

  def _append_(self, album):
    album._calculate_score_()
    self.__results__.append(album)

  def count(self, album):
    return len(self.__results__)

  def get_album(self, num):
    return self.__results__[num]

  def sort(self):
    self.__results__.sort()

  def do(self):
    tag = investigate.Tag(self.__folder__, self.__results__)
    self._append_(tag._do_album_())
    regexp = investigate.Regexp(self.__folder__, self.__results__)
    self._append_(regexp._do_album_())
    mix = investigate.Mix(self.__folder__, self.__results__)
    self._append_(mix._do_album_())
