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

from file_mp3 import FileMp3
from file_flac import FileFlac

class File:

  def __init__(self, folder, file_name):
    self._name_ =  file_name
    self._folder_ = folder
    self._fullpath_ = '%s/%s' % (folder._fullpath_, self._name_)
    self.__search_type__()
    self.__retrieve_extra_data__()
  
  def __cmp__(self, other):
    return cmp(self._name_, other._name_)

  def __search_type__(self):
    self._type_ = 'unknown'
    if '.jpg' in self._name_:
      self._type_ = 'jpg'
    elif '.mp3' in self._name_:
      self._type_ = 'mp3'
    elif '.ogg' in self._name_:
      self._type_ = 'ogg'
    elif '.flac' in self._name_:
      self._type_ = 'flac'
    elif '.m3u' in self._name_:
      self._type_ = 'm3u'
    elif '.sfv' in self._name_:
      self._type_ = 'sfv'
    elif '.nfo' in self._name_:
      self._type_ = 'nfo'

  def __retrieve_extra_data__(self):
    if self._type_ == 'mp3':
      self._extra_data_ = FileMp3(self)
    if self._type_ == 'flac':
      self._extra_data_ = FileFlac(self)

  def __str__(self):
    str = "file '%s' type '%s'" % (self._name_, self._type_)
    return str
