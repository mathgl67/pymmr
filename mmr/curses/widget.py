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

class Size(object):
  def __init__(self, w = -1, h = -1 ):
    self.width = w 
    self.height = h

  def is_valid(self):
    if self.width < 0:
      return False
    if self.height < 0:
      return False
    return True

  def __str__(self):
    return "(width=%d;height=%d)" % (self.width, self.height)

  def __add__(self, other):
    return Size(self.width + other.width, self.height + other.height)

  def __div__(self, other):
    return Size(self.width / other.width, self.height / other.height)

class Pos(object):
  def __init__(self, col = -1, line = -1):
    self.col = col
    self.line = line

  def is_valid(self):
    if self.col < 0:
      return False
    if self.line < 0:
      return False
    return True

  def __str__(self):
    return "(col=%d;line=%d)" % (self.col, self.line)



class Widget(object):
  def __init__(self):
    self._parent = None 
    self._handle = None
    self._pos = Pos(0,0) 
    self._size = Size(0,0)
    self._child_list = []
    self._event_list = {} 

  # getter
  def get_parent(self):
    return self._parent

  def get_parent_window(self):
    # this function is overide in window class to return
    # the window class. here we just have to call parent function
    # if there is a parent.
    if self._parent:
      return self._parent.get_parent_window()
    return None

  # setter
  def set_parent(self, parent):
    self._parent = parent

  def set_size(self, s):
    self._size = s

  def set_pos(self, p):
    self._pos = p

  # child management 
  def child_add(self, child):
    child.set_parent(self)
    self._child_list.append(child)

  def child_rm(self, child):
    self._child_list.remove(child)

  def child_clear(self):
    self._child_list = []

  # event management
  def event_add(self, e, f):
    self._event_list[e] = f

  def event_rm(self, e):
    del(self._event_list[e])

  def event_clear(self):
    self._event_list.clear() 

  # probe size
  def probe_size(self):
    size = Size(0, 0)
    for child in self._child_list:
      size = size + child.probe_size()
    return size

  # setup
  def setup(self):
    for child in self._child_list:
      child.setup()

  # display
  def display(self):
    for child in self._child_list:
      child.display()
  
  # refresh
  def refresh(self):
    for child in self._child_list:
      child.refresh()

  def event(self, e):
    # check my event
    if self._event_list.has_key(e):
      self._event_list[e]()

    # distribute to child
    for child in self._child_list:
      child.event(e)


