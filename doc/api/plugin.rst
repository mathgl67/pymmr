:mod:`mmr.plugin` -- Plugin related stuff 
=========================================

Introduction
------------

.. automodule:: mmr.plugin

Use exemple
-----------

Context
^^^^^^^

Imagine you have a directory with two plugins:

 * plugins

   * plugin1.py (available in system host)
   * plugin2.py (unavailable in system host)

Plugins source code
^^^^^^^^^^^^^^^^^^^

*plugin1.py*

 >>> from mmr.plugin import AbstractPlugin
 >>> class Plugin1(AbstractPlugin):
         def setup(self):
             self.type = "default"
             self.about = {
                 "name": u"Plugin1",
                 "short_description": u"A short plugin description",
                 "long_description": u"A long plugin description",
             }
          def available(self):
              return True
          

*plugin2.py*

 >>> from mmr.plugin import AbstractPlugin
 >>> class Plugin2(AbstractPlugin):
         def setup(self):
             self.type = "default"
             self.about = {
                 "name": u"Plugin1",
                 "short_description": u"A short plugin description",
                 "long_description": u"A long plugin description",
             }
         def available(self):
             return False

Load and use a plugin
^^^^^^^^^^^^^^^^^^^^^

 >>> import os
 >>> from mmr.plugin import PluginManager
 >>> pm = PluginManager(
              config={
                "path_list"=[u"plugins"],
              }
          )
 >>> pm.ensure_path_list_in_sys_path()
 >>> pm.load("plugin1")
 >>> pm["plugin1"].about


Module Contents
---------------

Utils
^^^^^

.. autofunction:: get_plugin_fullpath
.. autofunction:: get_plugin_path

Class :class:`AbstractPlugin`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: AbstractPlugin
      :show-inheritance:
      :members:

Class :class:`AbstractResearchPlugin`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: AbstractResearchPlugin
      :show-inheritance:
      :members:

Class :class:`PluginManager`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: PluginManager 
      :show-inheritance:
      :members:

