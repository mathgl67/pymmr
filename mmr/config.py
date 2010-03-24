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


class Config(object):
    """Config class"""
    def __init__(self, values={}):
        """Constructor: initialize data
            data -- a dictionary contains initialisation data
        """
        self.values = values

    def load(self, file_name):
        """Load configuration from a yaml file
            file_name -- the file name
        """
        self.values = yaml.load(open(file_name, "r").read(), Loader=Loader)

    def save(self, file_name):
        """Save configuration to a yaml file
            file_name -- the file name
        """
        file = open(file_name, "w+")
        yaml.dump(self.values, file, Dumper=Dumper, default_flow_style=False)
        file.close()

    def __getitem__(self, item):
        """Access values by using the dictionary operator.
           eg: config["item_name"]
            item -- item name
           Return the value for item.
        """
        return self.values[item]

    def __setitem__(self, item, value):
        """Write values by using the dictionary operator.
           eg: config["item_name"] = "value"
            item -- item name
            value -- value..
        """ 
        self.values[item] = value

    def has_key(self, item):
        """Proxy to the dictionary function"""
        return self.values.has_key(item)

