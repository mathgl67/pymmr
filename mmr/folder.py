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

import os
from file import *

class Folder:

  def __init__(self, fullpath):
    self._fullpath_ = fullpath
    self.__retrieve_dir_name__()
    self.__retrieve_file_list__()

  def __retrieve_dir_name__(self):
    str = self._fullpath_.split('/')
    self._name_ = str[len(str)-1]
    self._path_ = self._fullpath_.replace(self._name_, '')

  def __retrieve_file_list__(self):
    self._files_ = list()
    for f in os.listdir(self._fullpath_):
      file = File(self, f)
      self._files_.append(file)
    self._files_.sort()

  def __repr__(self):
    lines = []
    lines.append('<Folder name="%s" path="%s">' % (self._name_, self._path_))
    for f in self._files_:
      lines.append(repr(f))
    lines.append('</Folder>')
    return "\n".join(lines)

