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

from mmr.plugin import AbstractResearchPlugin
from mmr.album import Album
from mmr.track import Track
from mmr.abstract_investigate import AbstractInvestigate

class Lyric_wiki(AbstractResearchPlugin):
    def setup(self):
        self.investigate_class = LyricWikiInvestigate
        self.about = {
            "name": u"Lyric wiki",
            "short_description": u"",
            "long_description": u"",
        }
        self.priority = 5

    def available(self):
        try:
            import SOAPpy
        except ImportError as exception:
            return False
        return True

class LyricWikiInvestigate(AbstractInvestigate):
    def _set_up_(self):
        from SOAPpy import WSDL
        self._url_ = 'http://lyrics.wikia.com/server.php?wsdl'
        self._wsdl_ = WSDL.Proxy(self._url_)
        self._album_ = Album('lyric_wiki', self._base_score_)

    def do_album(self):
        for res in self._album_list_:
            if res.artist:
                result = self._wsdl_.getArtist(res.artist)

                match = False
                for album in result.albums:
                    if album['album'] == res.album:
                        match = True
                        self._album_.artist = res.artist
                        self._album_.album  = album['album']
                        self._album_.year = album['year']
                        index = 1
                        for song in album['songs']:
                            track = Track('lyric_wiki', self._base_score_)
                            track.tracknumber = index
                            track.title = song
                            self._tracks_[index] = track
                            index += 1

        return self._album_

    def do_track(self, file_obj, result_array):
        number = None
        title = None

        for result in result_array:
            if result.tracknumber:
                if result.tracknumber.find(u"/") is -1:
                    number = int(result.tracknumber)
                else:
                    num_array = result.tracknumber.split(u"/")
                    number = int(num_array[0])

            if result.title:
                title = result.title

            for index, track in self._tracks_.iteritems():
                if track.tracknumber == number:
                    return track
                if track.title == title:
                    return track

        return None
