import typing
from math import radians, cos, sin, asin, sqrt

from app.constellation.Constellation import Constellation
from app.constellation.StorePoint import StorePoint
from app.db import insert


class ConstellationFinder:
    ACCEPTABLE_DISTANCE = 5
    BOUNDARIES = [[-157.80430603, 17.69149971 ], [-64.70480347, 61.19303131]]

    def __init__(self, **kwargs):
        self.point_1: StorePoint = kwargs.get('point_1')
        self.point_2: StorePoint = kwargs.get('point_2')
        self.constellation: Constellation = kwargs.get('constellation')
        self.projected_constellation: typing.Optional[typing.List] = None
        self.minimum_constellation_size: float = kwargs.get('minimum_constellation_size', 500)

        self.store_lookup = kwargs.get('store_lookup')
        self.set_projected_constellation()

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

    @staticmethod
    def get_constellation_size(projected_constellation) -> float:
        max_x = max([c[0] for c in projected_constellation])
        max_y = max([c[1] for c in projected_constellation])
        min_x = min([c[0] for c in projected_constellation])
        min_y = min([c[1] for c in projected_constellation])
        return ConstellationFinder.haversine(max_x, max_y, min_x, min_y)

    def set_projected_constellation(self):
        projected_constellation = self.constellation.get_projected_constellation(self.point_1, self.point_2)
        if not self.is_constellation_within_boundary(projected_constellation):
            return
        if not self.get_constellation_size(projected_constellation) > self.minimum_constellation_size:
            return
        self.projected_constellation = projected_constellation

    def get_store_near_coordinates(self, coordinates) -> typing.Optional[StorePoint]:
        distance, point = self.store_lookup.get_nearest(coordinates)
        if ConstellationFinder.haversine_from_points(point, coordinates) <= ConstellationFinder.ACCEPTABLE_DISTANCE:
            return point

    def get_recursive_constellation(self, stores_in_constellation: typing.List):
        point_to_check = self.projected_constellation[len(stores_in_constellation)]
        closest_store = self.get_store_near_coordinates(point_to_check)
        if closest_store is None:
            return
        stores_in_constellation.append(closest_store)
        if len(stores_in_constellation) == len(self.projected_constellation):
            if len(set(stores_in_constellation)) == len(stores_in_constellation):
                return stores_in_constellation
            else:
                return
        return self.get_recursive_constellation(stores_in_constellation)

    def write_constellation(self, found_constellation: typing.List[StorePoint], size: float):
        insert(
            """
            INSERT INTO cf_raw_constellations (
                constellation_name, constellation_string, size, when_created
            ) VALUES (
                %(constellation_name)s,  %(constellation_string)s, %(size)s, CURRENT_TIMESTAMP
            )
            """, {
                'constellation_name': self.constellation.name,
                'constellation_string': '|'.join([x.get_store_id() for x in found_constellation]),
                'size': size
            }
        )

    def process(self) -> typing.Optional[float]:
        if self.projected_constellation is None:
            return
        found_constellation = self.get_recursive_constellation([])
        if found_constellation is None:
            return
        found_constellation_size = ConstellationFinder.get_constellation_size(found_constellation)
        if found_constellation_size < 100:
            return
        self.write_constellation(found_constellation, found_constellation_size)
        return found_constellation_size
