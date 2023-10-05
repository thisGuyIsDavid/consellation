import typing

from app.constellation.Constellation import Constellation
from app.constellation.StorePoint import StorePoint
from app.constellation.KDTree import KDTree
from math import radians, cos, sin, asin, sqrt
from app.db import insert_many
import uuid

class ConstellationFinder:

    ACCEPTABLE_DISTANCE = 25
    BOUNDARIES = [[-157.80430603, 17.69149971 ], [-64.70480347, 61.19303131]]

    def __init__(self, **kwargs):
        self.point_1: StorePoint = kwargs.get('point_1')
        self.point_2: StorePoint = kwargs.get('point_2')
        self.constellations: typing.List[Constellation] = kwargs.get('constellations')
        self.store_lookup = kwargs.get('store_lookup')
        self.projected_constellations: typing.List[typing.List] = []

        self.set_constellations()

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3956 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r

    @staticmethod
    def haversine_from_points(point_1, point_2):
        lon1, lat1 = point_1
        lon2, lat2 = point_2
        return ConstellationFinder.haversine(lon1, lat1, lon2, lat2)

    @staticmethod
    def is_constellation_within_boundary(projected_constellation) -> bool:
        #   Validate constellation is within boundary.
        if min([c[0] for c in projected_constellation]) < ConstellationFinder.BOUNDARIES[0][0]:
            return False
        if max([c[0] for c in projected_constellation]) > ConstellationFinder.BOUNDARIES[1][0]:
            return False
        if min([c[1] for c in projected_constellation]) < ConstellationFinder.BOUNDARIES[0][1]:
            return False
        if max([c[1] for c in projected_constellation]) > ConstellationFinder.BOUNDARIES[1][1]:
            return False
        return True

    def set_constellations(self):
        for constellation in self.constellations:
            projected_constellation = constellation.get_projected_constellation(self.point_1, self.point_2)
            if self.is_constellation_within_boundary(projected_constellation):
                self.projected_constellations.append([constellation.name, projected_constellation])

    def get_store_near_coordinates(self, coordinates) -> typing.Optional[StorePoint]:
        distance, point = self.store_lookup.get_nearest(coordinates)
        if ConstellationFinder.haversine_from_points(point, coordinates) <= ConstellationFinder.ACCEPTABLE_DISTANCE:
            return point

    def get_recursive_constellation(self, projected_constellation, stores_in_constellation: typing.List):
        point_to_check = projected_constellation[len(stores_in_constellation)]
        closest_store = self.get_store_near_coordinates(point_to_check)
        if closest_store is None:
            return
        stores_in_constellation.append(closest_store)
        if len(stores_in_constellation) == len(projected_constellation):
            if len(set(stores_in_constellation)) == len(stores_in_constellation):
                return stores_in_constellation
            else:
                return
        return self.get_recursive_constellation(projected_constellation, stores_in_constellation)

    def find(self):
        if len(self.projected_constellations) == 0:
            return
        for projected_constellation in self.projected_constellations:
            found_constellation = self.get_recursive_constellation(projected_constellation[1], [])
            if found_constellation is None:
                continue
            self.write_constellation(projected_constellation[0], found_constellation)

    def write_constellation(self, constellation_name, found_constellation: typing.List[StorePoint]):
        constellation_id = uuid.uuid4()
        insert_many(
            """
            INSERT INTO cf_constellations_found (
                constellation_name, constellation_uuid, store_id, when_created
            ) VALUES (
                %(constellation_name)s, %(constellation_uuid)s, %(store_id)s, CURRENT_TIMESTAMP
            )
            """, [
                {
                    'constellation_name': constellation_name,
                    'constellation_uuid': constellation_id,
                    'store_id': x.store_id
                } for x in found_constellation
            ]
        )

    @staticmethod
    def run():
        store_list = StorePoint.get_stores()
        store_lookup = KDTree(store_list, dim=2)
        constellations = Constellation.get_constellations()

        store_to_examine = StorePoint.get_store()
        while store_to_examine is not None:
            print(store_to_examine)
            for store_2 in store_list:
                if store_to_examine.store_id == store_2.store_id:
                    continue
                ConstellationFinder(
                    point_1=store_to_examine,
                    point_2=store_2,
                    constellations=constellations,
                    store_lookup=store_lookup
                ).find()
            store_to_examine.set_as_processed()
            store_to_examine = StorePoint.get_store()

if __name__ == '__main__':
    ConstellationFinder.run()