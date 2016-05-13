=====
Terms
=====

.. toctree::
    :hidden:
    :maxdepth: 1

    select
    transform
    manipulate
    aggregate
    geospatial

.. rubric:: Selecting data

=========================  ============================
Term                       Description
=========================  ============================
:ref:`$get`                Get a single document by its primary key
:ref:`$get_all`            Get all documents where the given value matches the requested index
:ref:`$filter`             Get all the documents for which the specified sequence is true
=========================  ============================


.. rubric:: Transformations

=========================  ============================
Term                       Description
=========================  ============================
:ref:`$with_fields`        Exclude documents that do not have the specified fields and return only those fields
:ref:`$has_fields`         Test if a document has the specified fields, filtering out any that do not
:ref:`$order_by`           Sort the documents by the specified field or index
:ref:`$skip`               Skip a number of documents from the head of the sequence
:ref:`$limit`              End the sequence after the givin number of documents
:ref:`$slice`              Return the documents within the specified range
:ref:`$nth`                Get the `nth` document in the sequence
:ref:`$sample`             Select a given number of elements from a sequence with uniform random distribution
=========================  ============================


.. rubric:: Manipulation

=========================  ============================
Term                       Description
=========================  ============================
:ref:`$pluck`              Return only the specified fields
:ref:`$without`            The opposite of ``$pluck``, return the documents without the specified fields
=========================  ============================


.. rubric:: Aggregation

=========================  ============================
Term                       Description
=========================  ============================
:ref:`$group`              Partition the documents into multiple groups based on the specified field
:ref:`$count`              Count the number of documents in the sequence
:ref:`$sum`                Sum the specified field of the sequence
:ref:`$avg`                Average the specified field of the sequence
:ref:`$min`                Find the minimum value of the specified field in the sequence
:ref:`$max`                Find the maximum value of the specified field of the sequence
=========================  ============================


.. rubric:: Geospatial

=========================  ============================
Term                       Description
=========================  ============================
:ref:`$get_intersecting`   Get all documents where the given geometry object intersects with a geometry object of a geospatial index
:ref:`$get_nearest`        Return the documents closest to the specified point based on a geospatial index
=========================  ============================
