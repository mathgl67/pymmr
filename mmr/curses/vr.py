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

import curses
from mmr.curses.widget import Widget, Size

class Vr(Widget):
  def __init__(self):
    super(Vr, self).__init__()
    self._max_size = False

  def set_max_size(self):
    self._max_size = True

  def probe_width(self):
    return 1 + super(Vr, self).probe_width()

  def _display_max_size(self):
    parent = self.get_parent()
    if parent:
      self._size = parent.get_max_size()

  def display(self):
    if self._max_size:
      self._display_max_size()

    window = self.get_parent_window()
    if window:
      window._handle.vline(self._pos.line, self._pos.col, curses.ACS_VLINE, self._size.height - 2)
      
    super(Vr, self).display()
