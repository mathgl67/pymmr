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
from mmr.curses.widget import Pos
from mmr.curses.window import Window
from mmr.curses.layout import VerticalLayout, HorizontalLayout
from mmr.curses.label import Label
from mmr.curses.text import Text
from mmr.curses.hr import Hr

class MessageBox(Window):
    def __init__(self):
        super(MessageBox, self).__init__()
        # set default
        self.title = ""
        self.text = ""

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def setup(self):
        layout = VerticalLayout()
        layout.set_probed()
        self.child_add(layout)

        title = Label()
        title.set_text(self.title)
        layout.child_add(title)

        hr = Hr()
        hr.set_max_size()
        layout.child_add(hr)

        text = Text()
        text.set_text(self.text)
        layout.child_add(text)

        hr2 = Hr()
        hr2.set_max_size()
        layout.child_add(hr2)
