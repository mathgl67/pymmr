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

from mmr.curses.widget import Widget, Size

class Label(Widget):
  def __init__(self, text=""):
    super(Label, self).__init__()
    self.text = text 

  def set_text(self, text):
    self.text = text    

  def probe_height(self):
    return 1 + super(Label, self).probe_height()

  def probe_width(self):
    return len(self.text) + super(Label, self).probe_width()

  def display(self):
    self.get_parent_window()._handle.addstr(self._pos.line, self._pos.col, self.text)
