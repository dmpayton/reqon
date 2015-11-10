import json
import dateutil.parser

from .geo import geojson_to_reql


def coerce(value):
    if isinstance(value, list) and len(value) == 2 and value[0] in COERSIONS:
        return COERSIONS[value[0]](value[1])
    return value


def coerce_datetime(value):
    '''
        ['$datetime', '1987-07-24 9:07pm']
    '''
    return dateutil.parser.parse(value)


def coerce_date(value):
    '''
        ['$date', '1987-07-24']
    '''
    return coerce_datetime(value).date()


def coerce_time(value):
    '''
        ['$time', '16:20']
    '''
    return coerce_datetime(value).time()


def coerce_geojson(value):
    if isinstance(value, basestring):
        value = json.loads(value)
    return geojson_to_reql(value)


COERSIONS = {
    '$date': coerce_date,
    '$time': coerce_time,
    '$datetime': coerce_datetime,
    '$geojson': coerce_geojson,
}
