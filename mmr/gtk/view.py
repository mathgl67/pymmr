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

class View(object):
    def __init__(self, view):
        self._view_ = view
        self.__init_render__()

    def __init_store__(self, store):
        self._store_ = store
        self._view_.set_model(self._store_)

    def __init_render__(self):
        self._render_ = {
          "text": gtk.CellRendererText(),
        }

    def __init_column__(self, name, type, id):
        col = gtk.TreeViewColumn(name)
        col.pack_start(self._render_[type], True)
        col.add_attribute(self._render_[type], type, id)
        self._view_.append_column(col)

    def __init_column_list__(self, list):
        for col in list:
            self.__init_column__(col['name'], col['type'], col['id'])

    def get_view(self):
        return self._view_

    def get_store(self):
        return self._store_

    def get_selected(self):
        selection = self._view_.get_selection()
        if selection:
            model, iter = selection.get_selected()
            return iter
        return None
