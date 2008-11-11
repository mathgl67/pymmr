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

import yaml

class Config:

    class __impl__:
        def __init__(self):
            self._file_ = None
            self._data_ = None
            self._file_name_ = None

        def load_file(self, file_name):
            self._file_name_ = file_name
            self._file_ = yaml.load(file(self._file_name_, 'rb').read())
            self._data_ = self._file_['pymmr']

        def __getattr__(self, attr):
            if self._data_.has_key(attr):
                return self._data_[attr]
            raise AttributeError, attr

    __instance__ = None

    def __init__(self):
        if Config.__instance__ is None:
            Config.__instance__ = Config.__impl__()
        self.__dict__['_Config__instance__'] = Config.__instance__

    def __getattr__(self, attr):
        return getattr(self.__instance__, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance__, attr, value)
