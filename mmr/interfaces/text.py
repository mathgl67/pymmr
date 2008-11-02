#!/usr/bin/env python
# vi:ai:et:ts=2 sw=2
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

import mmr

class Interface:

  def welcome(self):
    print "Welcome to My Music Renamer version %s" % (mmr.version)
    print "Copyright (C) 2007 mathgl67@gmail.com"
    print "My Music Renamer comes with ABSOLUTELY NO WARRANTY;"
    print "This is free software; Release under GPL;"
    print

