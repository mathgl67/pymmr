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
import os
from mmr.utils import DictProxy
from mmr.plugin import AbstractPlugin, AbstractResearchPlugin, PluginManager

class TestPlugin(unittest.TestCase):
    def assertNone(self, var):
        self.assertEquals(var, None)

    def assertIsInstance(self, var, cls):
        self.assertTrue(isinstance(var, cls))

    @staticmethod
    def suite():
        return unittest.TestSuite([
            # abstract plugin
            unittest.TestLoader().loadTestsFromTestCase(
                TestAbstractPluginConstructor
            ),
            unittest.TestLoader().loadTestsFromTestCase(
                TestAbstractResearchPluginConstructor
            ),
            # plugin manager
            unittest.TestLoader().loadTestsFromTestCase(
                TestPluginManagerConstructor
            ),
            unittest.TestLoader().loadTestsFromTestCase(
                TestPluginManagerValidateConfig
            ),
            unittest.TestLoader().loadTestsFromTestCase(
                TestPluginManagerPrePluginList
            ),
            unittest.TestLoader().loadTestsFromTestCase(
                TestPluginManagerLoad
            ),
        ])

# abstract plugin
class TestAbstractPluginConstructor(TestPlugin):
    def setUp(self):
        self.p = AbstractPlugin()

    def testDefaultType(self):
        self.assertIsInstance(self.p.about, dict)

    def testAboutDefault(self):
        self.assertNone(self.p.about["name"])
        self.assertNone(self.p.about["short_description"])
        self.assertNone(self.p.about["long_description"])

    def testTypeDefault(self):
        self.assertNone(self.p.type)

    def testAvailableDefault(self):
        self.assertTrue(self.p.available())

class TestAbstractResearchPluginConstructor(TestPlugin):
    def setUp(self):
        self.p = AbstractResearchPlugin()

    def testType(self):
        self.assertIsInstance(self.p.type, unicode)
        self.assertIsInstance(self.p.priority, int)

    def testDefault(self):
        self.assertEquals(self.p.type, u"research")
        self.assertEquals(self.p.priority, 0)
        self.assertNone(self.p.investigate_class)


# plugin manager
class TestPluginManagerConstructor(TestPlugin):
    def testDefaultType(self):
        pm = PluginManager()
        self.assertIsInstance(pm, DictProxy)
        self.assertIsInstance(pm.config, dict)
        self.assertIsInstance(pm.dict, dict)

    def testDefaultValue(self):
        pm = PluginManager()
        self.assertEquals(pm.config, {})
        self.assertEquals(pm.dict, {})

    def testSetConfig(self):
        config = { "test": True }
        pm = PluginManager(config=config)
        self.assertIsInstance(pm.config, dict)
        self.assertEquals(pm.config, config)
        self.assertEquals(pm.config['test'], True)

    def testNotSingleton(self):
        pm1 = PluginManager()
        pm2 = PluginManager()
        self.assertNotEquals(pm1, pm2)

class TestPluginManagerValidateConfig(TestPlugin):
    def testConfigInstance(self):
        pm = PluginManager(config=None)
        (status, message) = pm.validate_config()
        self.assertFalse(status)
        self.assertEquals(message, u"config must be a dict")

    def testPathListExists(self):
        pm = PluginManager(config={})
        (status, message) = pm.validate_config()
        self.assertFalse(status)
        self.assertEquals(message, u"'path_list' required")

    def testPathListInstance(self):
        pm = PluginManager(config={"path_list": None})
        (status, message) = pm.validate_config()
        self.assertFalse(status)
        self.assertEquals(message, u"'path_list' must be a list")

    def testGoodConfig(self):
        pm = PluginManager(config={"path_list": []})
        (status, message) = pm.validate_config()
        self.assertTrue(status)
        self.assertEquals(message, u"")


class TestPluginManagerPrePluginList(TestPlugin):
    def gen_config(self, path_list=[], black_list=[]):
        return {
            "path_list": path_list,
            "black_list": black_list,
        }

    def gen_pluginmanager(self, path_list=[], black_list=[]):
        return PluginManager(
            config=self.gen_config(path_list, black_list)
        )

    def gen_pre_pluginlist(self, path_list=[]):
        pm = self.gen_pluginmanager(path_list)
        return pm.pre_plugin_list()

    def testDirectoryNotExists(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"none")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 0)

    def testDirectoryContainsOneFile(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"one")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 1)
        self.assertEquals(pl[path][0], [u"", u"test1"])
    
    def testDirectoryContainsTwoFile(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"two")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 2)
        self.assertEquals(pl[path][0], [u"", u"test1"])
        self.assertEquals(pl[path][1], [u"", u"test2"])

    def testDirectoryContainsThreeFileRecurse(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 3)
        self.assertTrue([u"two", u"test2"] in pl[path])
        self.assertTrue([u"three", u"test3"] in pl[path])
        self.assertTrue([u"one", u"test1"] in pl[path])

class TestPluginManagerLoad(TestPluginManagerPrePluginList):
    def testOne(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"one")
        pm = self.gen_pluginmanager([path])
        pm.ensure_path_list_in_sys_path()
        pm.load_all()
        self.assertTrue(pm.has_key('test1'))
        self.assertIsInstance(pm['test1'], AbstractPlugin)

    def testThree(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pm = self.gen_pluginmanager([path])
        pm.ensure_path_list_in_sys_path()
        pm.load_all()
        self.assertEquals(len(pm), 3)
        self.assertTrue(pm.has_key('test1'))
        self.assertTrue(pm.has_key('test2'))
        self.assertTrue(pm.has_key('test3'))

    def testUnique(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pm1 = self.gen_pluginmanager([path], [u"test2"])
        pm2 = self.gen_pluginmanager([path], [u"test2"])
        self.assertNotEquals(pm1, pm2)

    def testWithBlackList(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pm = self.gen_pluginmanager([path], [u"test2"])
        pm.ensure_path_list_in_sys_path()
        pm.load_all()
        self.assertEquals(len(pm), 2)
        self.assertTrue(pm.has_key(u"test1"))
        self.assertFalse(pm.has_key(u"test2"))
        self.assertTrue(pm.has_key(u"test3"))

