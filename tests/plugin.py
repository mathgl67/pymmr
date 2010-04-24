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
import os, sys
from mmr.utils import DictProxy
from mmr.plugin import AbstractPlugin, AbstractResearchPlugin, PluginManager, get_plugin_fullpath, get_plugin_path

class TestPlugin(unittest.TestCase):
    def assertNone(self, var):
        self.assertEquals(var, None)

    def assertIsInstance(self, var, cls):
        self.assertTrue(isinstance(var, cls))

    @staticmethod
    def suite():
        classes = [
            TestAbstractPluginConstructor,
            TestAbstractResearchPluginConstructor,
            TestPluginBaseFunction,
            TestPluginManagerConstructor,
            TestPluginManagerValidateConfig,
            TestPluginManagerWalkForPlugin,
            TestPluginManagerLoad,
            TestPluginManagerLoadAll,
            TestPluginManagerFind,
        ]
        tests = []
        for cls in classes:
            tests.append(unittest.TestLoader().loadTestsFromTestCase(cls))

        return unittest.TestSuite(tests)

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

# base function
class TestPluginBaseFunction(TestPlugin):
    def testGetPluginFullpath(self):
        data = [
            {"path": u"", "name": u"test", "fullpath": u"test"},
            {"path": u"test", "name": u"test", "fullpath": u"test.test"},
            {"path": u"test.test2", "name": u"test3", "fullpath": u"test.test2.test3"},
        ]
        for test in data:
            self.assertEquals(
                test["fullpath"],
                get_plugin_fullpath(test["path"], test["name"])
            )

    def testGetPluginPath(self):
        data = [
            {"fullpath": u"research.my.plugin", "path": u"research.my"},
            {"fullpath": u"plugin", "path": u""},
            {"fullpath": u"my.plugin", "path": u"my"},
        ]
        for test in data:
            self.assertEquals(
                test["path"],
                get_plugin_path(test["fullpath"])
            )

# Plugin manager
class TestPluginManagerBase(TestPlugin):
    def gen_config(self, path_list=[], black_list=[], activate_list=[]):
        return {
            "path_list": path_list,
            "black_list": black_list,
            "activate_list": activate_list,
        }

    def gen_pluginmanager(self, path_list=[], black_list=[], activate_list=[]):
        return PluginManager(
            config=self.gen_config(path_list, black_list, activate_list)
        )

    def gen_pre_pluginlist(self, path_list=[]):
        pm = self.gen_pluginmanager(path_list)
        return pm._walk_for_plugin()

class TestPluginManagerConstructor(TestPluginManagerBase):
    def testDefaultType(self):
        pm = PluginManager()

    def testDefaultValue(self):
        pm = PluginManager()
        self.assertEquals(pm.config, {})
        self.assertEquals(pm, {})

    def testSetConfig(self):
        config = { "test": True }
        pm = PluginManager(config=config)
        self.assertIsInstance(pm.config, dict)
        self.assertEquals(pm.config, config)
        self.assertEquals(pm.config['test'], True)

    # this function is not in the good place
    def testEnsurePath(self):
        path = os.path.join("plugins", "path")
        pm1 = self.gen_pluginmanager([path])
        pm1.ensure_path_list_in_sys_path()
        self.assertTrue(path in sys.path)
    
class TestPluginManagerValidateConfig(TestPluginManagerBase):
    def testConfigInstance(self):
        pm = PluginManager()
        pm.config = None
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


class TestPluginManagerWalkForPlugin(TestPluginManagerBase):
    def testDirectoryNotExists(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"none")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 0)

    def testDirectoryContainsOneFile(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"one")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 1)
        self.assertTrue(u"test1" in pl[path])
    
    def testDirectoryContainsTwoFile(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"two")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 2)
        self.assertTrue(u"test1" in pl[path])
        self.assertTrue(u"test2" in pl[path])

    def testDirectoryContainsThreeFileRecurse(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pl = self.gen_pre_pluginlist([path])
        self.assertEquals(len(pl[path]), 3)
        self.assertTrue(u"two.test2" in pl[path])
        self.assertTrue(u"three.test3" in pl[path])
        self.assertTrue(u"one.test1" in pl[path])

class TestPluginManagerLoad(TestPluginManagerBase):
    def testOne(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"one")
        pm = self.gen_pluginmanager([path])
        pm.ensure_path_list_in_sys_path()
        pm.load("test1")
        self.assertTrue(pm.has_key("test1"))

    def testThree(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pm = self.gen_pluginmanager([path])
        pm.ensure_path_list_in_sys_path()
        pm.load("one.test1")
        self.assertTrue(pm.has_key("one.test1"))

class TestPluginManagerLoadAll(TestPluginManagerBase):
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
        self.assertTrue(pm.has_key('one.test1'))
        self.assertTrue(pm.has_key('two.test2'))
        self.assertTrue(pm.has_key('three.test3'))

    def testWithBlackList(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pm = self.gen_pluginmanager([path], [u"two.test2"])
        pm.ensure_path_list_in_sys_path()
        pm.load_all()
 
        self.assertEquals(len(pm), 2)
        self.assertTrue(pm.has_key(u"one.test1"))
        self.assertFalse(pm.has_key(u"two.test2"))
        self.assertTrue(pm.has_key(u"three.test3"))

    def testWithActivateList(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"three")
        pm = self.gen_pluginmanager([path], [], [u"two.test2"])
        self.assertFalse(pm.is_activate(u"one.test1"))
        self.assertTrue(pm.is_activate(u"two.test2"))
        self.assertFalse(pm.is_activate(u"three.test3"))

class TestPluginManagerFind(TestPluginManagerBase):
    def setUp(self):
        path = os.path.join(u"tests", u"data", u"plugins", u"find")
        activate = [ "t1p2", "t2p1" ]
        self.pm = self.gen_pluginmanager([path], [], activate)
        self.pm.ensure_path_list_in_sys_path()
        self.pm.load_all()

    def testTypeNotExist(self):
        pl = self.pm.find(
            plugin_type=u"type_not_exists",
            activate=False,
            available=False
        )
        self.assertEquals(len(pl), 0)

    def testType1All(self):
        pl = self.pm.find(
            plugin_type=u"type1",
            activate=False,
            available=False
        )
        self.assertEquals(len(pl), 2)
        self.assertTrue(self.pm["t1p1a"] in pl)
        self.assertTrue(self.pm["t1p2"] in pl)

    def testType2All(self):
        pl = self.pm.find(
            plugin_type=u"type2",
            activate=False,
            available=False
        )
        self.assertEquals(len(pl), 2)
        self.assertTrue(self.pm["t2p1"] in pl)
        self.assertTrue(self.pm["t2p2a"] in pl)

    def testType1Available(self):
        pl = self.pm.find(
            plugin_type=u"type1",
            activate=False,
            available=True
        )
        self.assertEquals(len(pl), 1)
        self.assertTrue(self.pm["t1p1a"] in pl)
        self.assertFalse(self.pm["t1p2"] in pl)

    def testType2Available(self):
        pl = self.pm.find(
            plugin_type=u"type2",
            activate=False,
            available=True
        )
        self.assertEquals(len(pl), 1)
        self.assertTrue(self.pm["t2p2a"] in pl)
        self.assertFalse(self.pm["t2p1"] in pl)

    def testType1Activate(self):
        pl = self.pm.find(
            plugin_type=u"type1",
            activate=True,
            available=False
        )
        self.assertEquals(len(pl), 1)
        self.assertTrue(self.pm["t1p2"] in pl)
        self.assertFalse(self.pm["t1p1a"] in pl)

    def testType2Activate(self):
        pl = self.pm.find(
            plugin_type=u"type2",
            activate=True,
            available=False
        )
        self.assertEquals(len(pl), 1)
        self.assertTrue(self.pm["t2p1"] in pl)
        self.assertFalse(self.pm["t2p2a"] in pl)
