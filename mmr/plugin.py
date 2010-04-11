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
This module contains all plugin related stuff.
"""

import os, sys

from mmr.utils import DictProxy


def get_plugin_fullpath(path, name):
    """
    Concatenate path and name (import style).

    :param path: a module path (can be empty) (eg: research.my_own )
    :type path: :class:`unicode`
    
    :param name: a module name (eg: plugin )
    :type name: :class:`unicode`
    
    :return: a the fullpath. (eg: research.my_own.plugin)
    :type: :class:`unicode`
    """
    if len(path) == 0:
        return name

    return "%s.%s" % (path, name)


def get_plugin_path(fullpath):
    """
    Get plugin path for a given fullpath (eg: research.own.plugin => research.own)

    :param fullpath: a plugin fullpath (eg: research.own.plugin)
    :type fullpath: :class:`unicode`

    :return: the plugin path (eg: research.own)
    :type: :class:`unicode`
    """
    path_list = fullpath.split(".")
    if len(path_list) == 1:
        return u""

    path_list = path_list[:-1]
    path = ".".join(path_list)
    
    return path

class AbstractPlugin(object):
    """
    This is the base class for plugin implementation.
    """

    type = None
    about = {
        "name": None,
        "short_description": None,
        "long_description": None,
    }

    def __init__(self):
        self.setup()

    def available(self):
        """
        Check if the plugin is available on the host system. (alias check dependency)
        @return True by default
        """
        return True

    def setup(self):
        """
        This fonction is called after the constructor. This is used to initialize the plugin.
        """


class AbstractResearchPlugin(AbstractPlugin):
    """
    This is the base class for research plugins.
    """
    priority = 0
    investigate_class = None
    type = u"research"

    def investigate(self, folder, album_list, config, base_score):
        """
        Create an investigate class for the plugin

        :return: an instance of AbstractInvestigate.
        """
        return self.investigate_class(folder, album_list, config, base_score)


class PluginManager(DictProxy):
    """
    This class contains plugin loading system.

    :param config: configuration values
    :type config: :class:`dict`

    :param values: the object can be pre-intialized
    :type values: :class:`dict`
    """
    def __init__(self, config={}, values={}):
        # call parent constructor
        super(PluginManager, self).__init__(values)
        # define config data
        self.config = config

    def validate_config(self):
        """
        Try to validate the config property.

        :return: (status, message) 
                 eg: [False, "the error message"]
        """
        # config must be a dict
        if not isinstance(self.config, dict):
            return [False, u"config must be a dict"]
        # check for needed keys
        if not self.config.has_key("path_list"):
            return [False, u"'path_list' required"]
        if not isinstance(self.config["path_list"], list):
            return [False, u"'path_list' must be a list"]
        
        return [True, u""]
    
    def load_all(self):
        """
        Load all plugin and store it in the dict
        """
        plugin_list = self._walk_for_plugin()
        self.dict = {} # really needed??
        for path in self.config['path_list']:
            for fullpath in plugin_list[path]:
                self.load(fullpath)

    def is_in_black_list(self, fullpath):
        """
        Check if plugin is in black list

        :param fullpath: the fullpath (eg: research.a_plugin)
        :type fullpath: :class:`unicode`

        :return: False or True
        """
        # no black list set
        if not self.config.has_key("black_list"):
            return False

        if not self.config["black_list"]:
            return False

        # search in black list
        if fullpath in self.config["black_list"]:
            return True

        return False
    
    def is_activate(self, fullpath):
        """
        Check if plugin is activate

        :param fullpath: the plugin full path (eg: research.own.plugin)
        :type fullpath: :class:`unicode`

        :return: True or False
        """
        if not self.config.has_key("activate_list"):
            return False

        if not self.config["activate_list"]:
            return False

        if fullpath in self.config["activate_list"]:
            return True

        return False

    def load(self, fullpath):
        """
        Load a given plugin and store it in dict.

        :param fullpath: the fullpath (eg: research.own.plugin)
        :type fullpath: :class:`unicode`

        :return: True or False
        """
        path = get_plugin_path(fullpath)

        #check blacklist
        if self.is_in_black_list(fullpath):
            return False

        # load
        module = __import__(
            fullpath,
            globals(),
            locals(),
            path.split('.')
        )

        if not module:
            return False 

        if not module.__dict__.has_key("plugin_class"):
            return False

        if not module.plugin_class:
            return False

        self.dict[fullpath] = module.plugin_class()
        self.dict[fullpath].fullpath = fullpath

        return True

    def ensure_path_list_in_sys_path(self):
        """
        Make sure all plugins path are in the sys.path.
        """
        for path in self.config["path_list"]:
            if not path in sys.path:
                sys.path.append(path.encode(sys.getfilesystemencoding()))

    def find(self, plugin_type=None, activate=True, available=True):
        """
        Retrieve a plugin list who meets some criteria.

        :param plugin_type: if not set as None, the plugin must have same type as specified.
        :type plugin_type: :class:`unicode`

        :param activate: if set as True then the plugin must be activate
        :type activate: :class:`boolean`

        :param available: if set as True then the plugin must be available
        :type available: :class:`boolean`

        :return: A list of plugin.
        """
        result = []
        # retrieve list
        for(fullpath, plugin) in self.iteritems():
            if available and not plugin.available():
                continue

            if activate and not self.is_activate(fullpath):
                continue

            if plugin_type and not plugin.type == plugin_type:
                continue

            result.append(plugin)

        # sort list by priority
        result.sort(cmp=lambda x, y: cmp(x.priority, y.priority))

        return result

    def _walk_for_plugin(self):
        """
        Create a list of plugin file by search for .py file in path_list.

        :return: a list of module for a path.
                eg : {path1: [fullpath1, ... ]}
        """
        result_dict = {}
        for path in self.config["path_list"]:
            result_dict[path] = [] 
            for (dir_path, dir_names, file_names) in os.walk(path):
                for file_name in file_names:
                    # check for python file
                    if not file_name.endswith(".py"):
                        continue

                    # ignore init file
                    if file_name.endswith("__init__.py"):
                        continue

                    # preparing module name
                    module_name = file_name.replace(".py", "")
                    # preparing path
                    # - remove starting path
                    module_path = dir_path.replace(path, u"")
                    # - remove root path
                    if module_path.startswith(os.path.sep):
                        module_path = module_path[1:]
                    # - import compatible
                    module_path = module_path.replace(os.path.sep, u".")
                    # store result in dict
                    result_dict[path].append(
                        get_plugin_fullpath(module_path, module_name)
                    )

        return result_dict

