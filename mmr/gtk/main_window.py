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
import threading
import copy

from mmr.folder import Folder
from mmr.album import Album
from mmr.plugin import PluginManager
from mmr.callback import Callback
from mmr.investigate_album import InvestigateAlbum
from mmr.gtk.error_message import ErrorMessage
from mmr.gtk.folder_view import FolderView
from mmr.gtk.album_view import AlbumView
from mmr.gtk.tracks_investigation_view import TracksInvestigationView
from mmr.gtk.tracks_view import TracksView
from mmr.gtk.plugin_manager import PluginManagerDialog

from fractions import Fraction

class MainWindow(object):
    def __init__(self, config):
        self.__init_builder__()
        self.__init_window__()
        self.__init_widgets__()
        self.__init_views__()

        self.config = config

        self.plugin_manager = PluginManager(copy.deepcopy(self.config["pluginmanager"]))
        self.plugin_manager.ensure_path_list_in_sys_path()
        self.plugin_manager.load_all()

        self._cur_folder_iter_ = None
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
          "progressbar1": self._builder_.get_object("progressbar1"),
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
        if self._cur_folder_iter_:
            # update album entry
            album = self._views_['folder'].get_album(self._cur_folder_iter_)
            if album:
                if album.artist:
                    self._widgets_["album"]["artist"].set_text(album.artist)
                else:
                    self._widgets_["album"]["artist"].set_text("")

                if album.album:
                    self._widgets_["album"]["album"].set_text(album.album)
                else:
                    self._widgets_["album"]["album"].set_text("")

                if album.genre:
                    self._widgets_["album"]["genre"].set_text(album.genre)
                else:
                    self._widgets_["album"]["genre"].set_text("")

                if album.year:
                    self._widgets_["album"]["year"].set_text(str(album.year))
                else:
                    self._widgets_["album"]["year"].set_text("")
            else:
                # blank it
                for key in ['artist', 'album', 'genre', 'year']:
                    self._widgets_['album'][key].set_text("")

            # update album_view
            self._views_['album'].clear()
            investigate_album = self._views_['folder'].get_investigate_album(self._cur_folder_iter_)
            if investigate_album:
                for result in investigate_album.result_list:
                    self._views_['album'].append(result)

    # signals
    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_menuitem_quit_activate(self, widget, data=None):
        gtk.main_quit()

    def on_button_investigate_clicked(self, widget, data=None):
        def on_module_start(self, module_name):
            self._widgets_['progressbar1'].set_text(module_name)

        def on_module_end(self, module_name):
            self._widgets_['progressbar1'].set_fraction(
                self._widgets_['progressbar1'].get_fraction() + self.step
            )
            self._widgets_['progressbar1'].set_text("Done")

        def thread(self):
            gobject.idle_add(widget.set_sensitive, False)

            self._widgets_['progressbar1'].set_fraction(0)
            self.step = Fraction(1, len(self.plugin_manager.find(u"research")))

            folder = self._views_['folder'].get_folder(self._cur_folder_iter_)
            investigate_album = InvestigateAlbum(
                config=self.config,
                folder=folder,
                plugin_manager=self.plugin_manager
            )
            investigate_album.cb_module_start = Callback(on_module_start, self)
            investigate_album.cb_module_end = Callback(on_module_end, self)
            investigate_album.investigate()
            investigate_album.result_list.sort()

            self._views_['folder'].set_investigate_album(
                self._cur_folder_iter_,
                investigate_album
            )

            gobject.idle_add(self._update_album_)
            gobject.idle_add(widget.set_sensitive, True)

        print "investigate"
        if self._cur_folder_iter_:
            thread = threading.Thread(target=thread, args = [self])
            thread.start()
           
    def on_button_validate_clicked(self, widget, data=None):
        print "validate!"
        if self._cur_folder_iter_:
            album = Album('validate')
            album.artist = self._widgets_['album']['artist'].get_text()
            album.album = self._widgets_['album']['album'].get_text()
            album.genre = self._widgets_['album']['genre'].get_text()
            try:
                album.year = int(self._widgets_['album']['year'].get_text())
            except:
                err = ErrorMessage("Cannot convert year to integer!")
                err.display()
            self._views_['folder'].set_album(self._cur_folder_iter_, album)

    def on_button_set_clicked(self, widget, data=None):
        print "set!"
        it = self._views_['album'].get_selected()
        if it and self._cur_folder_iter_:
            self._views_['folder'].set_album(self._cur_folder_iter_,
                self._views_['album'].get_album(it)
            )
            self._update_album_()

    def on_folder_view_row_activated(self, treeview, path, view_column):
        self._cur_folder_iter_ = self._views_['folder'].get_selected()
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
                folder = Folder.factory(folder_path)
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

    def on_toolbutton_list_investigate_clicked(self, widget, data=None):
        for it in self._views_["folder"].get_folder_iter_list():
            folder = self._views_['folder'].get_folder(it)
            investigate_album = InvestigateAlbum(
                config=self.config,
                folder=folder,
                plugin_manager=self.plugin_manager
            )
            investigate_album.investigate()
            investigate_album.sort()
            self._views_['folder'].set_investigate_album(it, investigate_album)

        self._update_album_()

    def on_menuitem_plugins_activate(self, widget, data=None):
        plugin_manager_dialog = PluginManagerDialog(self.config, self.plugin_manager)
        plugin_manager_dialog.show()
