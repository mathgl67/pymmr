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
from mmr.file import File

class Folder:
    def __init__(self, fullpath):
        self._name_ = None
        self._path_ = None
        self._files_ = None
        self._fullpath_ = fullpath

        self._retrieve_dir_name_()
        self._retrieve_file_list_()

        # this should be here ?
        self._album_ = None
        self._tracks_ = None

        self._investigate_album_ = None
        self._investigate_tracks_ = None
        # this should be here ?

    def _retrieve_dir_name_(self):
        path_array = self._fullpath_.split('/')
        self._name_ = path_array[len(path_array) - 1]
        self._path_ = self._fullpath_.replace(self._name_, '')

    def _retrieve_file_list_(self):
        self._files_ = []
        for file_path in os.listdir(self._fullpath_):
            file_obj = File.factory(os.path.join(self._fullpath_, file_path))
            self._files_.append(file_obj)
        self._files_.sort()

    def __repr__(self):
        lines = []
        lines.append('<Folder name="%s" path="%s">' % (self._name_,
                     self._path_))

        for file_obj in self._files_:
            lines.append(repr(file_obj))

        lines.append('</Folder>')
        return "\n".join(lines)

    def get_name(self):
        return self._name_

    def get_files(self):
        return self._files_

    def get_path(self):
        return self._path_

    def get_fullpath(self):
        return self._fullpath_
