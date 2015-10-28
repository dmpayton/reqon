================
Query descriptor
================

The ReQON query descriptor is an object with specific attributes:

.. code-block:: python

    {
        '$db': 'imdb',
        '$table': 'movies',
        '$query': [],
    }


.. _$db:

$db
===

References a specific database.

=====================  ==================
ReQON                  ReQL
=====================  ==================
``{'$db': 'imdb'}``    ``r.db('imdb')``
=====================  ==================

This attribute is optional.

.. _$table:

$table
======

Return all of the documents in the specified table of the default database.

=========================================  ==================================
ReQON                                      ReQL
=========================================  ==================================
``{'$table': 'movies'}``                   ``r.table('movies')``
``{'$db': 'imdb', '$table': 'movies'}``    ``r.db('imdb').table('movies')``
=========================================  ==================================

This attribute is required.


.. _$query:

$query
======

The query attribute is a sequence of :doc:`terms </terms/index>` that filter,
manipulate, or aggregate the document sequence in some way. Each term in the
sequence is a list of 1 or 2 items, where the first item is the name of the
term, followed (optionally, depending on the term) by a list of arguments.



This attribute is optional; omitting this attribute is the same as fetching
every document in the specified ``$table``.
