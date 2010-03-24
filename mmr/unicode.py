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

import locale
from os import path
import sys
from codecs import BOM_UTF8, BOM_UTF16_LE, BOM_UTF16_BE

def _getTerminalCharset():
    """
    Function used by getTerminalCharset() to get terminal charset.

    @see getTerminalCharset()
    """
    # (1) Try locale.getpreferredencoding()
    try:
        charset = locale.getpreferredencoding()
        if charset:
            return charset
    except (locale.Error, AttributeError):
        pass

    # (2) Try locale.nl_langinfo(CODESET)
    try:
        charset = locale.nl_langinfo(locale.CODESET)
        if charset:
            return charset
    except (locale.Error, AttributeError):
        pass

    # (3) Try sys.stdout.encoding
    if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
        return sys.stdout.encoding

    # (4) Otherwise, returns "ASCII"
    return "ASCII"

def getTerminalCharset():
    """
    Guess terminal charset using differents tests:
    1. Try locale.getpreferredencoding()
    2. Try locale.nl_langinfo(CODESET)
    3. Try sys.stdout.encoding
    4. Otherwise, returns "ASCII"

    WARNING: Call initUnicode() before calling this function.
    """
    try:
        return getTerminalCharset.value
    except AttributeError:
        getTerminalCharset.value = _getTerminalCharset()
        return getTerminalCharset.value

class UnicodeStdout(object):
    def __init__(self, old_device, charset):
        self.device = old_device
        self.charset = charset

    def flush(self):
        self.device.flush()

    def write(self, text):
        if isinstance(text, unicode):
            text = text.encode(self.charset, 'replace')
        self.device.write(text)

    def writelines(self, lines):
        for text in lines:
            self.write(text)

def initUnicode():
    # Only initialize locale once
    if initUnicode.is_done:
        return getTerminalCharset()
    initUnicode.is_done = True

    # Setup locales
    try:
        locale.setlocale(locale.LC_ALL, "")
    except (locale.Error, IOError):
        pass

    # Get the terminal charset
    charset = getTerminalCharset()

    # UnicodeStdout conflicts with the readline module
    if ('readline' not in sys.modules):
        # Replace stdout and stderr by unicode objet supporting unicode string
        sys.stdout = UnicodeStdout(sys.stdout, charset)
        sys.stderr = UnicodeStdout(sys.stderr, charset)
    return charset

initUnicode.is_done = False
