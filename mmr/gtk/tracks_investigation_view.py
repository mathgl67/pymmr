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

class TracksInvestigationView(View):
    def __init__(self, view):
        # view and model
        super(TracksInvestigationView, self).__init__(view)
        self.__init_store__(gtk.ListStore(str, int))
        # data
        self._investigation_list_ = {}
        # create cols
        self.__init_column_list__([
          {"name": "Name", "type": "text", "id": 0},
          {"name": "Score", "type": "text", "id": 1},
        ])

    def get_investigation(self, iter):
        iter_path = self._store_.get_string_from_iter(iter)
        return self._investigation_list_[iter_path]

    def append(self, investigation):
        iter = self._store_.append([
                investigation._investigater_,
                investigation._score_,
        ])

        iter_path = self._store_.get_string_from_iter(iter)
        self._investigation_list_[iter_path] = investigation

    def clear(self):
        self._store_.clear()
        self._investigation_list_ = {}
