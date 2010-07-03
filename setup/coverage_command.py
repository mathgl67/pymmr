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

import unittest
import coverage
from distutils.cmd import Command

class CoverageCommand(Command):
    description = "Tests coverage"
    user_options = [("html", None, "Generate html report")]
    
    def initialize_options(self):
        self.html = False

    def finalize_options(self):
        pass

    def run(self):
        cov = coverage.coverage()
        cov.erase()
        cov.start()
        # coverage have to be started before importing tests
        import tests
        from mmr import album, callback, config, file, folder, plugin
        from mmr.tags import abstract_tag, flac, mp3, ogg, tag

        # lauch tests silently
        ts = unittest.TestResult()
        tests.all_tests.run(ts)
        cov.stop()

       
        module_list = [
            album, callback, config, file, folder, plugin,
            abstract_tag, flac, mp3, ogg, tag
        ]

        cov.report(morfs=module_list)
        if self.html:
            cov.html_report(morfs=module_list, directory="coverage_html")
        
        coverage.erase()


