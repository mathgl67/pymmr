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

"""This file contain the Folder class"""

import sys
import os
from mmr.file import BaseFile

class Folder(object):
    """This is a Folder class"""

    def __init__(self, name=None, path=None, file_list=None):
        """Constructor"""
        self.name = name 
        self.path = path
        self.file_list = file_list

    def __repr__(self):
        """Return information on the Folder object"""
        lines = []
        lines.append(u"<Folder name='%(name)s' path='%(path)s'>" % {
            "name": self.name,
            "path": self.path,
        })

        if self.file_list:
            for file_obj in self.file_list:
                lines.append(file_obj.__repr__())

        lines.append(u"</Folder>")
        return u"\n".join(lines)

    def retrieve_file_list(self):
        """Retrieve the file list of the folder"""
        self.file_list = []
        for file_path in os.listdir(self.get_fullpath()):
            file_obj = BaseFile.factory(
                os.path.join(self.get_fullpath(), file_path)
            )
            self.file_list.append(file_obj)
        self.file_list.sort()

    def get_fullpath(self):
        """Return the fullpath of the folder"""
        return os.path.join(self.path, self.name)

    @staticmethod
    def factory(full_path):
        """Create and fill a Folder object"""
        folder = Folder()

        splited_path = os.path.split(full_path)
        folder.name = splited_path[1] 
        folder.path = splited_path[0]
        folder.retrieve_file_list()

        return folder
