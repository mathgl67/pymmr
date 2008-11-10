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

class File:
    def __init__(self, folder, file_name):
        self._name_ =  file_name
        self._folder_ = folder
        self._fullpath_ = '%s/%s' % (folder.get_fullpath(), self._name_)
        self._type_ = None
        self._extra_data_ = None

        self.__search_type__()
        self.__retrieve_extra_data__()

    def __cmp__(self, other):
        return cmp(self._name_, other.get_name())

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

    def get_name(self):
        return self._name_

    def get_type(self):
        return self._type_

    def get_tags(self):
        return self._extra_data_

    def get_fullpath(self):
        return self._fullpath_

    def __retrieve_extra_data__(self):
        self._extra_data_ = mmr.tags.Tag.get(self)

    def __repr__(self):
        return '<File name="%s" type="%s">' % (self._name_, self._type_)
