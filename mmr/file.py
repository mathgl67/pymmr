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

"""
This file contains all files related classes.
"""

import os
from mmr.tags.tag import Tag

class BaseFile(object):
    """
    This is the base file class.
    Used to represente file stocked in a :class:`mmr.folder.Folder`
    object.

    :param name: the file name (eg: file.ext)
    :type name: :class:`unicode`

    :param path: the file path (eg: /home/user)
    :type path: :class:`unicode`

    :param extension: the file extension (eg: .ext)
    :type extension: :class:`unicode`

    :param parent: the parent object (used?)
    :type parent: :class:`mmr.folder.Folder`
    """

    def __init__(self, name=None, path=None, extension=None, parent=None):
        """See class documentation"""
        self.path = path
        self.extension = extension
        self.parent = parent

    def __repr__(self):
        """Return representation of file"""
        return  u"<File name='%(name)s' extension='%(extension)s' path='%(path)s' />" % self.get_dict()

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
    def explore_meta_data(self):
        """
        This function do nothing.
        But it could be implemented by child class.
        This permit to call it in factory.
        """
        pass

    # factory
    @staticmethod
    def factory(fullpath):
        """This is the factory function of the file class.

           This function try to determine file type by using
           extension and instancy the most appropriate class.
           
           :param fullpath: the full path of the file.
           :type fullpath: :class:`unicode`

           :return: :class:`BaseFile` instance object
                    (:class:`BaseFile` or :class:`AudioFile`)
        """

        # define extension and class
        ext_class = {
          ".mp3": AudioFile,
          ".flac": AudioFile,
          ".ogg": AudioFile,
        }

        file_obj = None

        # retrieve base information
        splitpath = os.path.split(fullpath)
        name = splitpath[1]
        path = splitpath[0]
        extension = None

        # create a specific object if extension is found in dict
        splitext = os.path.splitext(fullpath)
        if not len(splitext[1]) == 0:
            extension = splitext[1]
            if extension in ext_class.keys():
                file_obj = ext_class[extension]()

        # else create a default object
        if not file_obj:
            file_obj = BaseFile()

        file_obj.name = name
        file_obj.path = path
        file_obj.extension = extension

        file_obj.explore_meta_data()

        return file_obj

class AudioFile(BaseFile):
    """
    This class is used to represent an audio file in a
    :class:`mmr.folder.Folder`. This simply add a

    The difference with the :class:`BaseFile` is the
    presence of the AudioFile.tags property.

    :param name: name of the file name
    :type name: :class:`unicode` 

    :param path: path of the file
    :type path: :class:`unicode`

    :param extension: the file extension
    :type extension: :class:`unicode`

    :param parent: the parent object (used?)
    :type parent: :class:`mmr.folder.Folder`
    """
    def __init__(self, name=None, path=None, extension=None, parent=None):
        """See class documentation"""
        super(AudioFile, self).__init__(name, path, extension, parent)
        self.tags = None

    def explore_meta_data(self):
        """
        This function explore audio file tag by using 
        :mod:`mmr.tags`.
        This function is called by the :func:`BaseFile.factory`
        function.
        """
        self.tags = Tag.get(self)

