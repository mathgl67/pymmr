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

from mmr.curses.widget import Widget, Size

class Text(Widget):
    def __init__(self):
        super(Text, self).__init__()
        self.text = ""

    def set_text(self, text):
        self.text = text

    def get_text_line_by_width(self):
        size = self.get_parent().get_max_size()
        tmp=""
        r=[]
        for ch in self.text:
            # max line size
            if len(tmp) == size.width - 2:
                r.append(tmp)
                tmp = ""
            # linejump
            if ch == '\n':
                r.append(tmp)
                tmp = ""
                continue
            tmp = tmp + ch
        r.append(tmp)
        return r

    def get_line_count(self):
        return self.text.count('\n')

    def get_text_line_by_height(self):
        size = self.get_parent().get_max_size()
        length = len(self.text)


        max_line = size.height - self.get_line_count()
        min_ch_by_line = len(self.text) / max_line

        r = []
        tmp = ""
        for ch in self.text:
            # max line size
            if len(tmp) == min_ch_by_line:
                r.append(tmp)
                tmp = ""
            # linejump
            if ch == '\n':
                r.append(tmp)
                tmp = ""
                continue
            tmp = tmp + ch
        r.append(tmp)

        return r

    def probe_height(self):
        height = len(self.get_text_line_by_width())
        return height + super(Text, self).probe_height()

    def probe_width(self):
        min_width = 0
        for line in self.get_text_line_by_height():
            if min_width <= len(line):
                min_width = len(line)

        return min_width + super(Text, self).probe_width()

    def display(self):
        max_size = self.get_parent().get_max_size()
        if max_size.width is -1:
            f = self.get_text_line_by_height
        else:
            f = self.get_text_line_by_width

        l = 0
        for line in f():
            print self._pos, line
            self.get_parent_window()._handle.addstr(self._pos.line+l, self._pos.col, line)
            l = l + 1

        super(Text, self).display()
