:mod:`mmr.config` -- Config's module operations 
===============================================

.. automodule:: mmr.config

Introduction
------------

This module contain the :class:`Config`.

Use exemples
------------

Read values
^^^^^^^^^^^

 >>> c = Config({u"a_parameter": True})
 >>> print c[u"a_parameter"]
 True

Set values
^^^^^^^^^^

 >>> c = Config()
 >>> c[u"a_parameter"] = True

Save values
^^^^^^^^^^^

 >>> c = Config({u"a_parameter": True})
 >>> c.save(u"a_config_file.yml") 

Load values
^^^^^^^^^^^

 >>> c = Config()
 >>> c.load(u"a_config_file.yml")
 >>> print c[u"a_parameter"]
 True


Module Contents
---------------

Class :class:`Config`
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Config 
      :show-inheritance:
      :members:

