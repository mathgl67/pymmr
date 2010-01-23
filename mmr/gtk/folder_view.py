#!/usr/bin/env python
# vi:ai:et:ts=4 sw=4
#
# -*- coding: utf8 -*-
#
# PyMmr My Music Renamer
# Copyright (C) 2007-2010  mathgl67@gmail.com
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

from mmr.gtk.view import View

class FolderView(View):
    def __init__(self, view):
        # view and model
        super(FolderView, self).__init__(view)
        self.__init_store__(gtk.ListStore(str, str))
        # create cols
        self.__init_column_list__([
          {"name": "Name", "type": "text", "id": 0},
          {"name": "Path", "type": "text", "id": 1},
        ])
        # data
        self._folder_list_ = {}
        self._album_list_ = {}
        self._investigate_album_list_ = {}

    def get_folder(self, it):
        iter_path = self._store_.get_string_from_iter(it)
        return self._folder_list_[iter_path]

    def get_folder_iter_list(self):
        r = []
        for key in self._folder_list_.keys():
            r.append(self._store_.get_iter_from_string(key))
        return r

    def get_album(self, it):
        iter_path = self._store_.get_string_from_iter(it)
        return self._album_list_[iter_path]

    def get_investigate_album(self, it):
        iter_path = self._store_.get_string_from_iter(it)
        return self._investigate_album_list_[iter_path]

    def set_album(self, it, album):
        iter_path = self._store_.get_string_from_iter(it)
        self._album_list_[iter_path] = album

    def set_investigate_album(self, it, investigate):
        iter_path = self._store_.get_string_from_iter(it)
        self._investigate_album_list_[iter_path] = investigate

    def append(self, folder):
        iter = self._store_.append([folder.name, folder.path])
        iter_path = self._store_.get_string_from_iter(iter)
        self._folder_list_[iter_path] = folder
        self._album_list_[iter_path] = None
        self._investigate_album_list_[iter_path] = None

    def remove(self, iter):
        iter_path = self._store_.get_string_from_iter(iter)
        del self._folder_list_[iter_path]
        self._store_.remove(iter)
