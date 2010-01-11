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

from mmr.curses.widget import Widget

class Label(Widget):
  def __init__(self):
    super(Label, self).__init__()
    self.text = "" 

  def set_text(self, text):
    self.text = text    

  def get_text_line_list(self):
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

  def display(self):
    l = 0
    for line in self.get_text_line_list():
      self.get_parent()._handle.addstr(self._pos.line+l, self._pos.col, line)
      l = l + 1

