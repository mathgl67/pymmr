#!/usr/bin/env python
# vi:ai:et:ts=4 sw=4
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

"""This file contain the File class"""

import os
from mmr.tags.tag import Tag

class File(object):
    """This class reprensent a file stored in a Folder"""

    def __init__(self, name=None, path=None, extension=None, parent=None):
        """Constructor function.
             name: set the file name (eg: file.ext)
             path: set the file path (eg: /home/user)
             extension: set the file extension (eg: .ext)"""
        self.name = name
        self.path = path
        self.extension = extension
        self.parent = parent

    def __str__(self):
        """Return representation of file"""
        return  "<File name='%{name}s' extension='%{extension}s' path='%{path}s' />" % self.get_dict()

    def get_dict(self):
        """Return a dict who dump all object data"""
        return {
          "name": self.name,
          "extension": self.extension,
          "path": self.path,
          "parent": self.parent,
        }

    def get_fullpath(self):
        """Return the object fullpath (eg: /home/user/file.ext)"""
        return os.path.join(self.path, self.name)

    # prototype function
    def _explore_meta_data_(self):
        """This functoin could be implemente by child class"""
        pass

    # factory
    @staticmethod
    def factory(fullpath):
        """This is the factory function of the file class.
           This look at the extension to determine a class to
           use (eg: AudioFile for mp3 file) and fill data"""

        # define extension and class
        ext_class = {
          ".mp3": FileAudio,
          ".flac": FileAudio,
          ".ogg": FileAudio,
        }

        file = None

        # retrieve base information
        splitpath = os.path.split(fullpath)
        name = splitpath[1]
        path = splitpath[0]
        extension = None

        # create a specific object if extension is found in dict
        splitext = os.path.splitext(fullpath)
        if splitext[1] is not "":
            extension = splitext[1]
            if extension in ext_class.keys():
                file = ext_class[extension]()

        # else create a default object
        if not file:
            file = File()

        file.name = name
        file.path = path
        file.extension = extension

        file._explore_meta_data_()

        return file

"""FileAudio class add a tags field"""
class FileAudio(File):
    def __init__(self):
        """define tags property"""
        super(FileAudio, self).__init__()
        self.tags = None

    def _explore_meta_data_(self):
        """This function explore audio file tag by using mmr.tags.
           This function is called by the File.factory static function."""
        self.tags = Tag.get(self)
