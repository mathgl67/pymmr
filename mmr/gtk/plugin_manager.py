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

import gtk
import gobject

class PluginManagerDialog(object):
    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.__init_builder__()
        self.__init_window__()
        self.__init_widgets__()
        self.__init_views__()

    def __init_builder__(self):
        # init builder
        self._interface_file_ = "mmr/gtk/plugin_manager.glade"
        try:
            self._builder_ = gtk.Builder()
            self._builder_.add_from_file(self._interface_file_)
        except:
            err = ErrorMessage("Cannot load interface file: %s" % (
              self._interface_file_
            ))
            err.display_and_exit()

    def __init_window__(self):
        self._window_ = self._builder_.get_object("plugin_manager")
        self._builder_.connect_signals(self)

    def __init_widgets__(self):
        self._widgets_ = {
            "plugin_list": self._builder_.get_object("plugin_list"),
        }

    def __init_views__(self):
        self._views_ = {
    		"plugin_manager": self._widgets_["plugin_list"].get_model(),
        }
        self._views_["plugin_manager"].clear()
        for (plugin_name, plugin) in self.plugin_manager.dict.iteritems():
            row = [plugin.available(), plugin.about["name"], plugin.about["short_description"]]
            self._views_["plugin_manager"].append(row)

    # util
    def show(self):
        self._window_.show()

    
