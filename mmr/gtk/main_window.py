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

import gtk

from mmr.folder import Folder
from mmr.album import Album
from mmr.investigate_album import InvestigateAlbum
from mmr.investigate_track import InvestigateTrack
from mmr.gtk.error_message import ErrorMessage
from mmr.gtk.folder_view import FolderView
from mmr.gtk.album_view import AlbumView
from mmr.gtk.tracks_investigation_view import TracksInvestigationView
from mmr.gtk.tracks_view import TracksView

class MainWindow(object):
  def __init__(self):
    self.__init_builder__()
    self.__init_window__()
    self.__init_widgets__()
    self.__init_views__()

    self._cur_folder = None
    self._statusbar_ctx_ = self._widgets_['statusbar'].get_context_id("StatusBar")

  def __init_builder__(self):
    # init builder
    self._interface_file_ = "mmr/gtk/main_window.glade"
    try:
      self._builder_ = gtk.Builder()
      self._builder_.add_from_file(self._interface_file_)
    except:
      err = ErrorMessage("Cannot load interface file: %s" % (
        self._interface_file_
      ))
      err.display_and_exit()
      
  def __init_window__(self):
    self._window_ = self._builder_.get_object("main_window")
    self._builder_.connect_signals(self)

  def __init_widgets__(self):
    self._widgets_ = {
      "statusbar": self._builder_.get_object("statusbar"),
      "folder_view": self._builder_.get_object("folder_view"),
      "album": {
        "artist": self._builder_.get_object("entry_artist"),
        "album": self._builder_.get_object("entry_album"),
        "genre": self._builder_.get_object("entry_genre"),
        "year": self._builder_.get_object("entry_year"),
      },
      "album_view": self._builder_.get_object("album_view"),
      "tracks_investigation_view": self._builder_.get_object("view_tracks_investigation"),
      "tracks_view": self._builder_.get_object("view_tracks_result"),
    }

  def __init_views__(self):
    self._views_ = {
      "folder": FolderView(self._widgets_["folder_view"]),
      "album": AlbumView(self._widgets_["album_view"]),
      "tracks_investigation": TracksInvestigationView(self._widgets_["tracks_investigation_view"]),
      "tracks_view": TracksView(self._widgets_["tracks_view"]),
    }

  # util
  def show(self):
    self._window_.show()

  def set_statusbar_text(self, text):
    self._widgets_['statusbar'].push(self._statusbar_ctx_, text)

  # update function
  def _update_album_(self):
    if self._cur_folder_:
      # update album entry
      album = self._cur_folder_._album_
      if album:
        if album.artist:
          self._widgets_['album']['artist'].set_text(album.artist)
        if album.album:
          self._widgets_['album']['album'].set_text(album.album)
        if album.genre:
          self._widgets_['album']['genre'].set_text(album.genre)
        if album.year:
          self._widgets_['album']['year'].set_text(str(album.year))

      # update album_view
      self._views_['album'].clear()
      if self._cur_folder_._investigate_album_:
        for result in self._cur_folder_._investigate_album_.__results__:
          self._views_['album'].append(result)
 
  # signals
  def on_main_window_destroy(self, widget, data=None):
    gtk.main_quit()

  def on_menuitem_quit_activate(self, widget, data=None):
    gtk.main_quit()

  def on_button_investigate_clicked(self, widget, data=None):
    print "investigate"
    if self._cur_folder_:
      self._cur_folder_._investigate_album_ = InvestigateAlbum(self._cur_folder_)
      self._cur_folder_._investigate_album_.investigate()
      self._cur_folder_._investigate_album_.sort()

      self._update_album_()
    
  def on_button_validate_clicked(self, widget, data=None):
    print "validate!" 
    if self._cur_folder_:
      self._cur_folder_._album_ = Album('validate')
      self._cur_folder_._album_.artist = self._widgets_['album']['artist'].get_text()
      self._cur_folder_._album_.album = self._widgets_['album']['album'].get_text()
      self._cur_folder_._album_.genre = self._widgets_['album']['genre'].get_text()
      try:
        self._cur_folder_._album_.year = int(self._widgets_['album']['year'].get_text())
      except:
        err = ErrorMessage("Cannot convert year to integer!")
        err.display()

  def on_button_set_clicked(self, widget, data=None):
    print "set!"
    iter = self._views_['album'].get_selected()
    if iter:
      self._cur_folder_._album_ = self._views_['album'].get_album(iter)
      self._update_album_()

  def on_folder_view_row_activated(self, treeview, path, view_column):
    iter = self._views_['folder'].get_selected()
    if iter:
      self._cur_folder_ = folder = self._views_['folder'].get_folder(iter)
      print "update to %s" % (self._cur_folder_._name_)
      # should update...
      self._update_album_()

  def on_toolbutton_list_add_clicked(self, widget, data=None):
    dialog = gtk.FileChooserDialog(
      title="Directory selection",
      parent=self._window_,
      action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
      buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
               gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    )
    response = dialog.run()
    if response == gtk.RESPONSE_ACCEPT:
      folder_path = dialog.get_filename()
      try:
        folder = Folder(folder_path)
        if folder:
          self._views_['folder'].append(folder)
      except:
        err = ErrorMessage("Cannot add floder: %s" % (folder_path))
        err.display()

    dialog.destroy()
  
  def on_toolbutton_list_rem_clicked(self, widget, data=None):
    iter = self._views_['folder'].get_selected()
    if iter:
      self._views_['folder'].remove(iter)

