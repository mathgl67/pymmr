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

import curses

from mmr.curses.window import Window

class Screen(Window):
    def __init__(self):
        super(Screen, self).__init__()
        self.exit = False

    def init(self):
        self._handle = curses.initscr()
        self._init_color()
        curses.noecho()
        curses.cbreak()
        self._handle.keypad(1)

    def _init_color(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def unload(self):
        if self._handle:
            curses.nocbreak()
            self._handle.keypad(0)
            curses.echo()
            curses.endwin()

    def set_exit(self):
        self.exit = True

    def get_ch(self):
        if self._handle:
            return self._handle.getch()
        return ''
