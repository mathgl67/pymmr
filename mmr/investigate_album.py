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

"""Contain InvestigateAlbum class"""

class InvestigateAlbum(object):
    """This class is used to investigate on album field"""

    def __init__(self, config=None, folder=None, plugin_manager=None):
        """Constructor"""
        self.config = config
        self.folder = folder
        self.plugin_manager = plugin_manager
        self.result_list = []
        self.cb_module_start = None
        self.cb_module_end = None

    def __repr__(self):
        """Return a string representation of the object"""
        lines = []
        lines.append(u"<InvestigateAlbum>")
        for res in self.result_list:
            lines.append(res.__repr__())
        lines.append(u"</InvestigateAlbum>")
        return u"\n".join(lines)

    def append(self, album):
        """append a result auto scored"""
        album.calculate_score()
        self.result_list.append(album)

    def do_module(self, module):
        """lauch a job for a module"""
        if self.cb_module_start:
            self.cb_module_start(module.about["name"])

        module_name = module.about["name"]

        # prepare module configuration
        module_config = {}
        if self.config.has_key(module_name):
            module_config = self.config[module_name]

        #base score
        base_score = self.config["score"]["default"]
        if self.config["score"].has_key(module_name):
            base_score = self.config["score"][module_name]

        investigate = module.investigate(
            self.folder,
            self.result_list,
            module_config,
            base_score
        )
        self.append(investigate.do_album())

        if self.cb_module_end:
            self.cb_module_end(module_name)

    def investigate(self):
        """Lauch investigation"""
        for module in self.plugin_manager.find(u"research"):
            self.do_module(module)

