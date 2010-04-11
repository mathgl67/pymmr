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
from mmr.abstract_investigate import AbstractInvestigate

class Musicbrainz(AbstractResearchPlugin):
    def setup(self):
        self.investigate_class = MusicbrainzInvestigate
        self.about = {
            "name": u"Musicbrainz",
            "short_description": u"",
            "long_description": u"",
        }
        self.priority = 5 

    def available(self):
        try:
            import musicbrainz2
        except ImportError as exception:
            return False
        return True

plugin_class=Musicbrainz

class MusicbrainzInvestigate(AbstractInvestigate):
    def _set_up_(self):
        self._album_ = Album('musicbrainz', self._base_score_)

    def do_album(self):
    	from musicbrainz2.webservice import Query, ArtistFilter, ReleaseFilter, WebServiceError
        from musicbrainz2.utils import extractUuid

        for res in self._album_list_:
            artist_id = None
            if res.artist:
                q = Query()
                try:
                    f = ArtistFilter(name=res.artist)
                    artistsResults = q.getArtists(f)
                    for result in artistsResults:
                        artist = result.artist
                        if result.score is 100:
                            artist_id = extractUuid(artist.id)
                            print "found artist_id:", artist_id
                except WebServiceError, e:
                    print u"ERROR:", e 
           
            if res.artist and res.album:
                q = Query()
                try:
                    f = ReleaseFilter(
                        artistId=artist_id,
                        artistName=res.artist,
                        title=res.album
                    )
                    releaseResults = q.getReleases(f)
                    for result in releaseResults:
                        release = result.release
                        self._album_.artist = release.artist.name
                        self._album_.album = release.title
                        self._album_.genre = release.artist.type
                        self._album_.year = release.getEarliestReleaseDate()
                except WebServiceError, e:
                    print u"ERROR:", e

        return self._album_

    def do_track(self, file_obj, result_array):
        return None
