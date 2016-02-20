==========================
ReQL Query Object Notation
==========================

.. image:: https://travis-ci.org/dmpayton/reqon.svg?branch=develop
    :target: https://travis-ci.org/dmpayton/reqon
    :alt: travis-ci.org

.. image:: https://codeclimate.com/github/dmpayton/reqon/badges/gpa.svg
    :target: https://codeclimate.com/github/dmpayton/reqon
    :alt: codeclimate.com

.. image:: https://codecov.io/github/dmpayton/reqon/coverage.svg?branch=develop
    :target: https://codecov.io/github/dmpayton/reqon?branch=develop
    :alt: codecov.io

ReQON ([ɹiːˈkʰɑn], /riːˈkɑn/, RE-kon) lets you build simple, read-only `RethinkDB <http://rethinkdb.com/>`_
queries from JSON.

I love RethinkDB, and ReQL is awesome and powerful, but sometimes you need to
expose RethinkDB's querying capabilities through an HTTP API endpoint. ReQON
lets you do that.

ReQON transforms this:

.. code-block:: python

    {
        '$table': 'movies',
        '$query': [
            ['$filter', [
                ['rating', ['$gt', 8]],
                ['$or', [
                    ['year', ['$lt', 1990]],
                    ['year', ['$gt', 1999]]
                ]]
            ]],
            ['$order_by', ['$asc', 'rank'],
            ['$sample', 5]
        ]
    }

into this:

.. code-block:: python

    r.table('movies').filter(
        r.row['rating'] > r.expr(8),
        r.or_(
            r.row['year'] < r.expr(1990),
            r.row['year'] > r.expr(1999),
        )
    ).order_by(r.asc('rank'))
    ).sample(5)


ReQON makes it easy to query RethinkDB through a web API:

.. code-block:: python

    import json
    import reqon
    import rethinkdb as r


    class QueryEndpoint(View):
        def post(self, request):
            conn = r.connect()
            query = json.loads(request.body)
            reql = reqon.query(query)
            results = reql.run(conn)
            conn.close()
            return json.dumps({'data': results})
