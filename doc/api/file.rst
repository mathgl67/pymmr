:mod:`mmr.file` -- File's module operations 
===========================================

.. automodule:: mmr.file

Introduction
------------

All file object sould be intanciate by the factory function (:func:`mmr.file.factory`). The function will automatic choose the best class to represent the file (:class:`BaseFile` or :class:`AudioFile`).

Use exemples
------------
 
 >>> import mmr.file
 >>> f = mmr.file.factory("tests/data/tags/silence.flac")
 >>> print isinstance(f, mmr.file.AudioFile) 
 True

Module Contents
---------------

Function :func:`factory`
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: factory

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

