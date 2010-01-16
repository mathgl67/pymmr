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

from mmr.gtk.folder_store import FolderStore
from mmr.gtk.album_store import AlbumStore

class Main:
  # signals
  def on_main_window_destroy(self, widget, data=None):
    gtk.main_quit()

  def on_menuitem_quit_activate(self, widget, data=None):
    gtk.main_quit()

  def on_button_investigate_clicked(self, widget, data=None):
    print "investigate"
    if self._cur_folder:

      self._cur_folder._investigate_album_ = mmr.InvestigateAlbum(self._cur_folder)
      self._cur_folder._investigate_album_.investigate()
      self._cur_folder._investigate_album_.sort()

      self.update_album()
    
  def on_button_validate_activate(self, widget, data=None):
    pass

  def on_button_set_clicked(self, widget, data=None):
    print "set!"
    selection = self.album_view.get_selection()
    if selection:
      model, iter = selection.get_selected()
      if iter:
        self._cur_folder._album_ = self.album_store.get_album(iter)
        self.update_album()

  def on_folder_view_row_activated(self, treeview, path, view_column):
    selection = self.folder_view.get_selection()
    if selection:
      model, iter = selection.get_selected()
      if iter:
        self._cur_folder = self.folder_store.get_folder(iter)
        print "update to %s" % (self._cur_folder._name_)
        # should update...
        self.update_album()

  def on_toolbutton_list_add_clicked(self, widget, data=None):
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
      folder = mmr.Folder(folder_path)
      if folder:
        self.folder_store.append(folder)

    dialog.destroy()
  
  def on_toolbutton_list_rem_clicked(self, widget, data=None):
    self.selection = self.folder_view.get_selection()
    if self.selection:
      model, iter = self.selection.get_selected()
      if iter:
        self.folder_store.remove(iter)

  def on_imagemenuitem_list_investigate_activate(self, widget, data=None):
    self.test = "" 

  # update
  def update_album(self):
    if self._cur_folder:
      # update album entry 
      if self._cur_folder._album_:
        self.entry_artist.set_text(self._cur_folder._album_.artist)
        self.entry_album.set_text(self._cur_folder._album_.album)
        self.entry_genre.set_text(self._cur_folder._album_.genre)
        self.entry_year.set_text(str(self._cur_folder._album_.year))

      # update album_view
      self.album_store.clear()
      if self._cur_folder._investigate_album_:
        for result in self._cur_folder._investigate_album_.__results__:
          self.album_store.append(result)
  
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

    # create a text render
    self.cell_render_text = gtk.CellRendererText()

    self.folder_view = builder.get_object("folder_view")
    self.interface_folder_view_init()

    self.entry_artist = builder.get_object("entry_artist")
    self.entry_album = builder.get_object("entry_album")
    self.entry_genre = builder.get_object("entry_genre")
    self.entry_year = builder.get_object("entry_year")

    self.album_view = builder.get_object("album_view")
    self.interface_album_view_init()

    builder.connect_signals(self)

  def interface_folder_view_init(self):
    self.folder_store = FolderStore() 
    self.folder_view.set_model(self.folder_store)
    self.folder_col = {}
    self.folder_col['Name'] = self.interface_init_col_text(self.folder_view, 'Name', 0) 
    self.folder_col['Path'] = self.interface_init_col_text(self.folder_view, 'Path', 1)

  def interface_init_col_text(self, tree, name, id):
    col = gtk.TreeViewColumn(name)
    col.pack_start(self.cell_render_text, True)
    col.add_attribute(self.cell_render_text, 'text', id)
    tree.append_column(col)
    return col

  def interface_album_view_init(self):
    self.album_store = AlbumStore()
    self.album_view.set_model(self.album_store)

    self.album_col = {} 
    self.album_col['Name'] = self.interface_init_col_text(self.album_view, 'Name', 0)
    self.album_col['Score'] = self.interface_init_col_text(self.album_view, 'Score', 1)
    self.album_col['Artist'] = self.interface_init_col_text(self.album_view, 'Artist', 2)
    self.album_col['Album'] = self.interface_init_col_text(self.album_view, 'Album', 3)
    self.album_col['Genre'] = self.interface_init_col_text(self.album_view, 'Genre', 4)
    self.album_col['Year'] = self.interface_init_col_text(self.album_view, 'Year', 5)

  def __init__(self):
    self._cur_folder = None

    self.interface_load()
    self.config_load()

  
  def run(self):
    self.main_window.show()
    gtk.main()


