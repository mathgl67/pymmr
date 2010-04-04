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

"""This file contains some utilities"""

class DictProxy(object):
    """
    This class is not directly used. It make child class
    to be accecing like a dictionary. And provide some
    utilities fonction.

    :param values: initialisation values.
    :type values: :class:`dict`
    """
    def __init__(self, values={}):
        """See class documentation"""
        self.dict = values

    # getter, setter
    def __getitem__(self, key):
        """
        Access values by using the dictionary operator.
        eg: config["item_name"]

        :param key: the key name
        :type key: :class:`unicode`

        :return: the value stored at the key in the dict.
        """
        return self.dict[key]

    def __setitem__(self, key, value):
        """
        Write values by using the dictionary operator.
        eg: config["item_name"] = "value"

        :param key: the key name
        :type key: :class:`unicode`

        :param value: the value
        """ 
        self.dict[key] = value

    def __len__(self):
        return len(self.dict)

    # iteration
    def iteritems(self):
        return self.dict.iteritems()
        
    def iterkeys(self):
        return self.dict.iterkeys()
        
    def itervalues(self):
        return self.dict.itervalues()

    # dictionary fonction
    def has_key(self, key):
        """
        Check in the :class:`dict` if key exist. This is
        a proxy function.

        :param key: the key name
        :type key: :class:`unicode`

        :return: False or True (:class:`bool`)
        """
        return self.dict.has_key(key)

