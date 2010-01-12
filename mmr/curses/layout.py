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

from mmr.curses.widget import Widget, Pos, Size

class Layout(Widget):
  pass

class VerticalLayout(Layout):
  def __init__(self):
    super(VerticalLayout, self).__init__()
    self._shared = False
    self._max_size = None

  def set_shared(self):
    self._shared = True

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

  def display(self):
    if self._shared:
      self._display_shared()
   
    super(VerticalLayout, self).display()


