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

import mmr
from abstract_investigate import AbstractInvestigate

from xml.dom import minidom, Node

import urlparse, httplib, urllib

class Investigate(AbstractInvestigate):
    def _setUp_(self):
        self._album_ = mmr.Album('lyric_wiki')

    def _do_album_(self):
        url = urlparse.urlparse('http://lyricwiki.org')
        resource = 'api.php'
        args = { 'func':'getArtist', 'fmt': 'xml', 'artist': '' }

        for res in self._album_list_:
            if res.artist:
                args['artist'] = res.artist.encode('UTF-8')
                path = '/%s?%s' % (resource, urllib.urlencode(args))
                conn = httplib.HTTPConnection(url.netloc)
                conn.request('GET', path)
                resp = conn.getresponse()
                dom = minidom.parseString(resp.read())
                albums = dom.getElementsByTagName('albums').item(0)

                match = False
                for node in albums.childNodes:
                    if (node.nodeType == Node.ELEMENT_NODE and
                        node.tagName == 'album'):
                        match = False
                        if node.firstChild.data == res.album:
                            match = True
                            self._album_.artist = res.artist
                            self._album_.album  = res.album
                        elif (node.tagName == 'year' and match and
                              node.firstChild):
                            self._album_.year = node.firstChild.data

            return self._album_