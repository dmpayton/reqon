==============
Selecting data
==============


.. _$get:

$get
====

.. py:function:: get(key)

See also: http://rethinkdb.com/api/python/get/

.. _$get_all:

$get_all
========

.. py:function:: get_all(keys[, index])

See also: http://rethinkdb.com/api/python/get_all/


.. _$filter:

$filter
=======

.. py:function:: filter(predicate)

==================  ============  ============================================
Boolean operator    ReQL          See also:
==================  ============  ============================================
``$and``            ``r.and_``    http://rethinkdb.com/api/python/and/
``$or``             ``r.or_``     http://rethinkdb.com/api/python/or/
``$not``            ``r.not_``    http://rethinkdb.com/api/python/not/
==================  ============  ============================================

See also: http://rethinkdb.com/api/python/filter/


.. _$between:

$between
========

.. py:function:: between(lower_key, upper_key[, index, left_bound, right_bound])
