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

import mmr

from mmr.curses.screen import Screen
from mmr.curses.messagebox import MessageBox
from mmr.curses.widget import Size

class Main:
  def __init__(self):
    self._screen = Screen()
    self._interface = None
    self._interface_list = []
    self._interface_curent = 0

  def loop(self):
    self._screen.init()
    while self._interface:
      self._screen.clear()
      self._screen.child_clear()
      self._screen.child_add(self._interface)

      self._screen.setup()
      self._screen.display()
      self._screen.refresh() 

      e = self._screen.get_ch()
      self._screen.event(e)
 
    self._screen.unload()

  def interface_add(self, interface):
    self._interface_list.append(interface)
    self.interface_update()

  def interface_update(self):
    if self._interface_curent >= len(self._interface_list):
      self._interface = None
      return
    self._interface = self._interface_list[self._interface_curent]

  def interface_next(self):
    self._interface_curent = self._interface_curent + 1
    self.interface_update()

  def welcome(self):
    # prepare
    mb = MessageBox()
    mb.set_title("Welcome to My Music Renamer version %s" % (mmr.MMR['version']))
    mb.set_text("Copyright (C) 2007 mathgl67@gmail.com\nMy Music Renamer comes with ABSOLUTELY NO WARRANTY;\nThis is free software; Release under GPL;")
#    mb.set_max_size()
    mb.set_size(Size(80,25))
    mb.set_center()
    mb.event_add(ord(' '), self.interface_next)

    return mb


  def win2(self):
    mb = MessageBox()
    mb.set_title("Windows 2 Title")
    mb.set_text("blablablabla")
    mb.set_max_size()
    mb.event_add(ord(' '), self.interface_next)

    return mb
    
  def run(self):
    self.interface_add(self.welcome())
    self.interface_add(self.win2())
    self.loop()

