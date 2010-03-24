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

class Loader:
    _modules_ = {}
    @staticmethod
    def load_by_name(name, folder, album_list, config, base_score):
#        if Loader._modules_.has_key(name):
#            return Loader._modules_[name]

        module = __import__("mmr.investigate.%s" % (name),
                            globals(), locals(), ["mmr", "investigate"])

        Loader._modules_[name] = module.Investigate(folder, album_list, config, base_score)
        return Loader._modules_[name]
