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

from mmr.config import Config
from mmr.investigate.loader import Loader


class InvestigateAlbum(object):
    """This class is used to investigate on album field"""

    def __init__(self, folder=None):
        """Constructor"""
        self.folder = folder
        self.result_list = []

    def __str__(self):
        """Return a string representation of the object"""
        lines = []
        lines.append(u"<InvestigateAlbum>")
        for res in self.result_list:
            lines.append(str(res))
        lines.append(u"</InvestigateAlbum>")
        return u"\n".join(lines)

    def append(self, album):
        """append a result auto scored"""
        album.calculate_score()
        self.result_list.append(album)

    def iteration(self, module_name):
        pass

    def investigate(self):
        """Lauch investigation"""
        for module_name in Config().investigater:
            module = Loader.load_by_name(module_name, self.folder,
                                         self.result_list)
            self.iteration(module_name)
            self.append(module.do_album())

