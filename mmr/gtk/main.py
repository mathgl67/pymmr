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

class Main:
  # signals
  def on_main_window_destroy(self, widget, data=None):
    gtk.main_quit()

  def on_menuitem_quit_activate(self, widget, data=None):
    gtk.main_quit()

  def on_menuitem_open_activate(self, widget, data=None):
    dialog = gtk.FileChooserDialog(
      title="Directory selection",
      parent=self.main_window,
      action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
      buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
               gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    )
    response = dialog.run()
    if response == gtk.RESPONSE_ACCEPT:
      folder_path = dialog.get_filename() 
      self.statusbar_push("Analyse folder: %s ..." % folder_path)
      self.folder = mmr.folder.Folder(folder_path)
      self.statusbar_push("Analyse folder: %s done." % folder_path)

      self.statusbar_push("Investigate on Album")
      self.investigate_album = mmr.InvestigateAlbum(self.folder)
      self.investigate_album.investigate()
      self.statusbar_push("Investigate on Album done.")

      # update investigator
      for result in self.investigate_album.__results__:
        self.investigator_store.append(None, [result._investigater_, result._score_, result.artist, result.album, result.genre, result.year])

    dialog.destroy()

  # helper function
  def error_message(self, message):
    # print on console
    print message
    # graphical error display
    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
    dialog.run()
    dialog.destroy()

  def statusbar_push(self, text):
    self.statusbar.push(self.statusbar_ctx, text)

  # initialize
  def config_load(self):
    #load config file
    try:
      self.config = mmr.Config()
      self.config.load_file('pymmr.cfg')
      self.statusbar_push("Config file loaded.")
    except:
      self.error_message("Cannot load config file: pymmr.cfg") 
      sys.exit(1)

  def interface_load(self):
    self.interface_file = "mmr/gtk/gmmr.glade"

    try:
      builder = gtk.Builder()
      builder.add_from_file(self.interface_file)
    except:
      self.error_message("Failed to load UI XML file: %s" % (self.interface_file))
      sys.exit(-1)

    self.main_window = builder.get_object("main_window")

    self.statusbar = builder.get_object("statusbar")
    self.statusbar_ctx = self.statusbar.get_context_id("StatusBar")

    self.investigator_tree = builder.get_object("investigator_view")
    self.interface_init_investigator()

    builder.connect_signals(self)

  def interface_init_investigator_col(self, name, id):
    self.investigator_col[name] = gtk.TreeViewColumn(name)
    self.investigator_col[name].pack_start(self.cell, True)
    self.investigator_col[name].add_attribute(self.cell, 'text', id)
    self.investigator_tree.append_column(self.investigator_col[name])

  def interface_init_investigator(self):
    self.investigator_store = gtk.TreeStore(str, str, str, str, str, str)
    self.investigator_tree.set_model(self.investigator_store)

    self.cell = gtk.CellRendererText()

    self.investigator_col = {} 
    self.interface_init_investigator_col('Name', 0)
    self.interface_init_investigator_col('Score', 1)
    self.interface_init_investigator_col('Artist', 2)
    self.interface_init_investigator_col('Album', 3)
    self.interface_init_investigator_col('Genre', 4)
    self.interface_init_investigator_col('Year', 5)

  def __init__(self):
    self.interface_load()
    self.config_load()

  
  def run(self):
    self.main_window.show()
    gtk.main()


