====================
ReQL Object Notation
====================

ReQLON (/'rɛklən/) lets you build basic `ReQL <http://rethinkdb.com/docs/introduction-to-reql/>`_
queries from JSON.

I love RethinkDB, and ReQL is awesome and powerful, but sometimes you need to
expose RethinkDB's querying capabilities through an HTTP API endpoint.

ReQLON transforms this:

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


Do you want to expose RethinkDB through an HTTP API? ReQLON is for you.

.. code-block:: python

    import json
    import reqlon
    import rethinkdb as r


    class QueryEndpoint(View):
        def post(self, request):
            conn = r.connect()
            query = json.loads(request.body)
            reql = reqlon.query(query)
            results = reql.run(conn)
            conn.close()
            return json.dumps({'data': results})
