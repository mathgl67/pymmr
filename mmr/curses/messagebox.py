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
from mmr.curses.widget import Pos
from mmr.curses.window import Window
from mmr.curses.label import Label

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
    label = Label()
    label.set_text(self.text)
    label.set_pos(Pos(1, 3))
    self.child_add(label)

  def display(self):
    super(MessageBox, self).display()
    self._handle.hline(2, 1, curses.ACS_HLINE, self._size.width - 2)
    self._handle.addstr(1,1, self.title)
   
