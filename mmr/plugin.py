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

"""This module contains all plugin related stuff."""

import os, sys

from mmr.utils import DictProxy

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
        plugin_list = self.pre_plugin_list()
        self.dict = {} # really needed??
        for path in self.config['path_list']:
            for (module_path, module_name) in plugin_list[path]:
                if not module_name in self.config["black_list"]:
                    self.dict[module_name] = self.load(module_path, module_name)

    def load(self, module_path, module_name):
        """
        Load a giving module an return it instance.

        :param module_path: the module path (eg: my.research)
        :type module_path: :class:`unicode`

        :param module_name: the module name (eg: test)
        :type module_name: :class:`unicode`

        :return: None on errors, or an instance of :class:`AbstractPlugin`
        """
        if module_path == u"":
            module_fullpath = module_name
        else:
            module_fullpath = "%s.%s" % (
                module_path,
                module_name
            )

        module = __import__(
            module_fullpath,
            globals(),
            locals(),
            module_path.split('.')
        )

        if not module:
            return None

        if not module.__dict__.has_key(module_name.capitalize()):
            return None

        return module.__dict__[module_name.capitalize()]()

    def ensure_path_list_in_sys_path(self):
        """
        Make sure all plugins path are in the sys.path.
        """
        for path in self.config["path_list"]:
            if not path in sys.path:
                sys.path.append(path.encode(sys.getfilesystemencoding()))

    def available_research(self):
        """
        Retrieve all research plugins stored in dict and sort it by priority.

        :return: A list of plugin.
        """
        result = []
        # retrieve list
        for value in self.itervalues():
            if value.available() and value.type == "research":
                result.append(value)
        # sort list by priority
        result.sort(cmp=lambda x,y: cmp(x.priority, y.priority))
        return result

    def pre_plugin_list(self):
        """
        Create a list of plugin file by search for .py file in path_list.

        :return: a list of module for a path.
                eg : {path1: [[module_path1, module_name1], ... ]}
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
                    result_dict[path].append([module_path, module_name])

        return result_dict

