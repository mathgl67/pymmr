#!/usr/bin/env python
# vi:ai:et:ts=2 sw=2
#
# -*- coding: utf8 -*-
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

import sys
from optparse import OptionParser

import mmr

from mmr.config import Config
from mmr.folder import Folder
from mmr.investigate_album import InvestigateAlbum
from mmr.investigate_track import InvestigateTrack

class Main:
  def __init__(self):
    pass

  def run(self):
    self.welcome()
    self.parse_args()
    self.load_config()
    self.folder()
    self.test()

  def welcome(self):
    print "Welcome to My Music Renamer version %s" % (mmr.MMR['version'])
    print "Copyright (C) 2007 mathgl67@gmail.com"
    print "My Music Renamer comes with ABSOLUTELY NO WARRANTY;"
    print "This is free software; Release under GPL;"
    print


  def parse_args(self):
    """Parse commande line arguments"""

    #init argv parser
    usage = "usage: %prog [options] <music_directory>"
    parser = OptionParser(usage=usage, version="%s %s" % (
      mmr.MMR['prog'],
      mmr.MMR['version']
    ))

    #add option
    parser.add_option(
      "-v", "--verbose", action="store_true", dest="verbose", default=False,
      help="make lot of noise"
    )

    parser.add_option(
      "-c", "--config", dest="config", default="pymmr.cfg",
      help="Use a specific config file"
    )

    #parse
    (self.options, self.args) = parser.parse_args()
  
    #check args
    if len(self.args) < 1:
      parser.print_help()
      sys.exit(1)

  def load_config(self):
    #load config file
    try:
      self.config = Config()
      self.config.load_file(self.options.config)
    except:
      print 'could not load/parse config file (%s)' % self.options.config
      sys.exit(1)

  def folder(self):
    if self.options.verbose:
      print "Folder: analyse '%s'..." % (self.args[0])

    self.folder = Folder(self.args[0])
    if self.options.verbose:
      print "Folder: done. result..."
      print self.folder.__repr__().encode('UTF-8')


  def album(self):
    pass 

  def test(self):
    investigate_album = InvestigateAlbum(self.folder)
    investigate_album.investigate()
    investigate_album.sort()

    print investigate_album.__repr__().encode('UTF-8')
    print

    investigate_track = InvestigateTrack(self.folder)
    investigate_track.investigate()
    
    print investigate_track.__repr__().encode('UTF-8') 

