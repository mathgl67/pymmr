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

import sys 
import mmr

# Display a fatal error when gtk is not installed.
try:
  import gtk
except ImportError as exception:
  print "FATAL: Gtk python module is require and must be installed." 
  sys.exit(1)

from mmr.gtk.main_window import MainWindow
from mmr.gtk.error_message import ErrorMessage

class Main:
  # initialize
  def _config_load_(self):
    #load config file
    try:
      self._config_ = mmr.Config()
      self._config_.load_file("pymmr.cfg")
      self._main_window_.set_statusbar_text("Config file loaded.")
    except:
      err = ErrorMessage("Cannot load config file: pymmr.cfg")
      err.display_and_exit()

  def __init__(self):
    self._main_window_ = MainWindow()
    self._config_load_()
  
  def run(self):
    self._main_window_.show()
    gtk.main()

