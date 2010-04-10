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
    def __init__(self, config, plugin_manager):
        self.config = config
        self.plugin_manager = plugin_manager
        self._init_builder()
        self._init_widget()
        self._init_view()

    def _init_builder(self):
        # init builder
        self._interface_file = "mmr/gtk/plugin_manager.glade"
        try:
            self._builder = gtk.Builder()
            self._builder.add_from_file(self._interface_file)
            self._builder.connect_signals(self)
        except:
            err = ErrorMessage("Cannot load interface file: %s" % (
              self._interface_file
            ))
            err.display_and_exit()

    def _init_widget(self):
        self.dialog = self._builder.get_object("dlg_plugin_manager")
        self.view_plugin = self._builder.get_object("view_plugin")
        self.model_plugin = self.view_plugin.get_model()

    def _init_view(self):
        self.update_plugin()

    def _gobj_from_plugin(self, plugin):
        gobj = gobject.GObject()
        gobj.set_data("plugin", plugin)
        return gobj

    def _gobj_to_plugin(self, gobj):
        return gobj.get_data("plugin")

    def _get_plugin_by_row(self, row):
        return self._gobj_to_plugin(self.model_plugin.get_value(row.iter, 0))

    def update_plugin(self):
        self.model_plugin.clear()
        for (plugin_fullpath, plugin) in self.plugin_manager.dict.iteritems():
            row = [self._gobj_from_plugin(plugin), self.plugin_manager.is_activate(plugin_fullpath), plugin.available(), plugin.about["name"], plugin.about["short_description"]]
            self.model_plugin.append(row)

    # util
    def show(self):
        self.dialog.show()
   
    def on_cellrenderertoggle2_toggled(self, widget, row):
        row = self.model_plugin[row]
        plugin = self._get_plugin_by_row(row)

        if self.plugin_manager.is_activate(plugin.fullpath):
            self.plugin_manager.config["activate_list"].remove(plugin.fullpath)
        else:
            self.plugin_manager.config["activate_list"].append(plugin.fullpath)
        self.update_plugin()
        

    def on_btn_cancel_clicked(self, widget, data=None):
        self.dialog.destroy()

    def on_btn_okay_clicked(self, widget, data=None):
        print "save..."
        self.config.save()
        self.dialog.destroy()
