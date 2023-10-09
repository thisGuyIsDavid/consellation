import typing

from app.constellation.ConstellationFinder import ConstellationFinder
from app.db import get_all_rows, update_many


def translate_points(point_string):
    stores = get_all_rows(
        """
        SELECT id, company_name, latitude, longitude FROM store_list
        """
    )
    stores_as_lookup = {str(p['id']): p for p in stores}

    points = []
    for store in point_string.split('|'):
        store_deats = stores_as_lookup.get(store)
        print(store_deats['company_name'])
        points.append([store_deats['longitude'], store_deats['latitude']])

    print('const points =', points)


def get_constellation_string_as_points(constellation_string: str, store_lookup: typing.Dict):
    points = []
    for store in constellation_string.split('|'):
        store_deats = store_lookup.get(store)
        points.append([store_deats['longitude'], store_deats['latitude']])
    return points


def set_size_of_points():
    stores = get_all_rows(
        """
        SELECT id, company_name, latitude, longitude FROM store_list
        """
    )
    stores_as_lookup = {str(p['id']): p for p in stores}
    points = get_all_rows(
        """
        SELECT id, constellation_string
        FROM cf_raw_constellations
        WHERE size IS NULL
        ORDER BY when_created DESC
        LIMIT 1000
        """
    )
    if len(points) == 0:
        return
    to_update = []

    for point in points:
        as_coordinates = get_constellation_string_as_points(point.get('constellation_string'), stores_as_lookup)
        to_update.append(
            {
                'id': point['id'],
                'size': ConstellationFinder.get_constellation_size(as_coordinates)
            }
        )

    update_many(
        """
        UPDATE cf_raw_constellations
        SET size = %(size)s
        WHERE id = %(id)s
        """,
        to_update
    )
    return len(to_update)

translate_points('5856887|565244|565274|2919435|7643985|417423|72064|417468|7561810|565831|2985502|565954|565997|2953672|1991436|1701332|7820687')
