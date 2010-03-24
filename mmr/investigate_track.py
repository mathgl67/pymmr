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

from mmr.config import Config
from mmr.investigate.loader import Loader

class InvestigateTrack:
    def __init__(self, folder, config):
        self.config = config
        self._folder_ = folder
        self._results_ = {}
        self._init_result_()

    def _init_result_(self):
        for file_obj in self._folder_.file_list:
            self._results_[file_obj.name] = []


    def __repr__(self):
        lines = []
        lines.append(u"<InvestigateTrack>")
        for file_name, result in self._results_.items():
            lines.append(u"<File name=\"%s\">" % unicode(file_name,
                'ISO8859-15')) # should not be here.. !
            for track in result:
                lines.append(track.__repr__())
            lines.append(u"</File>")
        lines.append(u"</InvestigateTrack>")
        return u"\n".join(lines)

    def investigate(self):
        for module_name in self.config['investigater']:
            #retrieve config ...
            module_config = {}
            if self.config.has_key(module_name):
                module_config = self.config[module_name]

            #base score
            base_score = self.config["score"]["default"]
            if self.config["score"].has_key(module_name):
                base_score = self.config["score"][module_name]

            # load module
            module = Loader.load_by_name(module_name, self._folder_,
                                         self._results_, module_config,
                                         base_score)

            for file_obj in self._folder_.file_list:
                track = module.do_track(file_obj, self._results_[file_obj.name])
                if track:
                    track.calculate_score()
                    self._results_[file_obj.name].append(track)
