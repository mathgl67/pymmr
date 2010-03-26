:mod:`mmr.file` -- File's module operations 
===========================================

.. automodule:: mmr.file

Introduction
------------

All file object sould be intanciate by the factory function (:func:`mmr.file.BaseFile.factory`). The function will automatic choose the best class to represent the file (:class:`BaseFile` or :class:`AudioFile`).

Use exemples
------------
 
 >>> from mmr.file import BaseFile, AudioFile
 >>> f = BaseFile.factory("tests/data/tags/silence.flac")
 >>> print isinstance(f, AudioFile) 
 True

Module Contents
---------------

Class :class:`BaseFile`
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: BaseFile
      :show-inheritance:
      :members:

Class :class:`AudioFile`
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: AudioFile
      :show-inheritance:
      :members:

