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

"""This module contains all related module stuff."""

import os, sys

from mmr.utils import DictProxy

class AbstractPlugin(object):
    def __init__(self):
        self.type = None
        self.about = {
            "name": None,
            "short_description": None,
            "long_description": None,
        }
        self.setup()

    def available(self):
        return True

    def setup(self):
        pass


class AbstractResearchPlugin(AbstractPlugin):
    def __init__(self):
        self.priority = 0
        self.investigate_class = None
        super(AbstractResearchPlugin, self).__init__()
        self.type = u"research"

    def investigate(self, folder, album_list, config, base_score):
        return self.investigate_class(folder, album_list, config, base_score)


class PluginManager(DictProxy):
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
        plugin_list = self.pre_plugin_list()
        self.dict = {} # really needed??
        for path in self.config['path_list']:
            for (module_path, module_name) in plugin_list[path]:
                if not module_name in self.config["black_list"]:
                    self.dict[module_name] = self.load(module_path, module_name)

    def load(self, module_path, module_name):
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
        for path in self.config["path_list"]:
            if not path in sys.path:
                sys.path.append(path.encode(sys.getfilesystemencoding()))

    def available_research(self):
        result = []
        # retrieve list
        for value in self.itervalues():
            if value.available() and value.type == "research":
                result.append(value)
        # sort list by priority
        result.sort(cmp=lambda x,y: cmp(x.priority, y.priority))
        return result

    def pre_plugin_list(self):
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

