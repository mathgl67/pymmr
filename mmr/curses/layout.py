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

from mmr.curses.widget import Widget, Pos, Size

class Layout(Widget):
    pass

class VerticalLayout(Layout):
    def __init__(self):
        super(VerticalLayout, self).__init__()
        self._shared = False
        self._probed = False
        self._max_size = None

    def set_shared(self):
        self._shared = True

    def set_probed(self):
        self._probed = True

    def get_max_size(self):
        return self._max_size

    def _display_shared(self):
        child_nbr = len(self._child_list)
        size_div = Size(child_nbr,child_nbr)
        parent = self.get_parent()
        if parent:
            size = parent.get_max_size()
            shared_size = size / size_div

            self._max_size = Size(size.width, shared_size.height)

            line_pos = 1
            for child in self._child_list:
                child.set_pos(Pos(1, line_pos))
                line_pos = line_pos + shared_size.height

    def _display_probed(self):
        size = self.get_parent().get_max_size()
        self._max_size = Size(size.width, -1)

        cur_line = 1
        for child in self._child_list:
            print cur_line, child.probe_height()
            child.set_pos(Pos(1, cur_line))
            cur_line = cur_line + child.probe_height()

    def _display_manual(self):
        self._max_size = self.get_parent().get_max_size()

    def display(self):
        if self._shared:
            self._display_shared()
        elif self._probed:
            self._display_probed()
        else:
            self._display_manual()

        super(VerticalLayout, self).display()


class HorizontalLayout(Layout):
    def __init__(self):
        super(HorizontalLayout, self).__init__()
        self._shared = False
        self._probed = False
        self._max_size = None

    def get_max_size(self):
        return self._max_size

    def set_probed(self):
        self._probed = True

    def set_shared(self):
        self._shared = True

    def _display_shared(self):
        pass

    def _display_probed(self):
        size = self.get_parent().get_max_size()
        self._max_size = Size(-1, size.height)

        cur_col = 1
        for child in self._child_list:
            child.set_pos(Pos(cur_col, 1))
            cur_col = cur_col + child.probe_width()


    def display(self):
        if self._shared:
            self._display_shared()
        elif self._probed:
            self._display_probed()

        super(HorizontalLayout, self).display()
