==========================
ReQL Query Object Notation
==========================

ReQON (/ˈriːkɒn/) lets you build basic `ReQL <http://rethinkdb.com/docs/introduction-to-reql/>`_
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
