#!/usr/bin/env python
# vi:ai:et:ts=4 sw=4
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

import curses

from mmr.curses.widget import Widget, Pos, Size

class Window(Widget):
    def __init__(self):
        super(Window, self).__init__()
        self._center = False
        self._max_size = False

    # setter
    def set_max_size(self):
        self._max_size = True

    def set_center(self):
        self._center = True


    # getter
    def get_parent_window(self):
        # overide default Widget function
        # to return me to child
        return self

    def get_max_size(self):
        size = Size()
        if self._handle:
            (size.height, size.width) = self._handle.getmaxyx()
        return size

    # create
    def create_subwin(self, size, pos):
        if self._handle:
            return self._handle.derwin(size.height, size.width, pos.line, pos.col)
        return None

    # display delayed
    def _display_center(self):
        parent_size = self.get_parent().get_max_size()
        self.set_pos(Pos(parent_size.width / 2 - self._size.width / 2,
                         parent_size.height / 2 - self._size.height /2))

    def _display_max_size(self):
        if self._parent:
            self.set_size(self.get_parent().get_max_size())
            return True
        return False

    # display
    def display(self):
        # task before display
        if self._center:
            self._display_center()

        if self._max_size:
            self._display_max_size()

        # display a window
        # must be safe: screen doesn't have parent
        if self._parent:
            self._handle = self._parent.create_subwin(self._size, self._pos)
            self._handle.box()


        # call parent
        super(Window, self).display()

    # refresh
    def refresh(self):
        super(Window, self).refresh()
        if self._handle:
            return self._handle.refresh()
        return None

    def clear(self):
        if self._handle:
            return self._handle.clear()
