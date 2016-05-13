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

ReQON ([ɹiːˈkʰɑn], /riːˈkɑn/, RE-kon) lets you build simple, read-only
`RethinkDB <http://rethinkdb.com/>`_ queries from JSON.

I love RethinkDB, and ReQL is awesome and powerful, but sometimes you need to
expose RethinkDB's querying capabilities through an HTTP API endpoint. ReQON
lets you do that.

ReQON transforms this:

.. code-block:: python

    {
        '$table': 'movies',
        '$query': [
            ['$filter', {'predicate': [
                ['rating', ['$gt', 8]],
                ['$or', [
                    ['year', ['$lt', 1990]],
                    ['year', ['$gt', 1999]]
                ]]
            ]}],
            ['$order_by', {'index': 'rank', 'ordering': 'asc'}],
            ['$sample', {'n': 5}]
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
            # Open a RethinkDB connection
            conn = r.connect()

            # Build the query from the POST body
            query = json.loads(request.body)
            reql = reqon.query(query)

            # Get the results and close the connection
            results = reql.run(conn)
            if isinstance(results, r.Cursor):
                results = list(results)
            conn.close()
            return HttpResponse(json.dumps({'data': results}))
