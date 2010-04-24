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

# Display a fatal error when yaml is not installed.
# Yaml is require to parse the config file.
try:
    import yaml
except ImportError as exception:
    print "FATAL: Yaml python module is require and must be installed. (python-yaml)"
    import sys
    sys.exit(1)

# try to load the libyaml Loader and Dumper
# describe to be more faster
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import sys
import codecs

class Config(dict):
    """
    This class is used for configutation operation
    ( Loading, saving, accessing configuration values ).
    """

    def load(self, file_name):
        """
        Load configuration from a yaml file

        :param file_name: the yaml file
        :type file_name: :class:`unicode`
        """
        file = codecs.open(
            file_name,
            "r",
            sys.getfilesystemencoding()
        )
        if file:
            self.clear()
            self.update(
                yaml.load(
                    file.read(),
                    Loader=Loader
                )
            )
            file.close()
            self.previous_file = file_name

    def save(self, file_name=None):
        """
        Save configuration to a yaml file.
        In case no file is given, the fonction take
        the previous loaded file.

        :param file_name: the yaml file (optional)
        :type file_name: :class:`unicode`
        """
        if not file_name:
            file_name = self.previous_file

        file = codecs.open(
            file_name,
            "w+",
            sys.getfilesystemencoding()
        )
        yaml.dump(
            self,
            file,
            Dumper=Dumper,
            default_flow_style=False
        )
        file.close()

