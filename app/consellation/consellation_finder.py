import time
import typing
from math import radians, cos, sin, asin, sqrt

from app.consellation.constellation_utils import get_projected_constellation
from kd_tree import KDTree
from store_list import StorePoint


class ConsellationFinder:

    ACCEPTABLE_DISTANCE = 25

    def __init__(self, constellation_name,  constellation_points):
        self.constellation_name: str = constellation_name
        self.store_list: typing.List[StorePoint] = []
        self.store_kd_tree: typing.Optional[KDTree] = None
        self.constellation_points: list = constellation_points

        #   Boundaries
        self.boundary_fails:int = 0
        self.x_max: typing.Optional[float] = None
        self.x_min: typing.Optional[float] = None
        self.y_max: typing.Optional[float] = None
        self.y_min: typing.Optional[float] = None

    def set_store_points(self):
        self.store_list = StorePoint.get_stores()
        self.store_kd_tree = KDTree(self.store_list, dim=2)

    def set_boundaries(self):
        self.x_min = min([s.x for s in self.store_list])
        self.x_max = max([s.x for s in self.store_list])
        self.y_min = min([s.y for s in self.store_list])
        self.y_max = max([s.y for s in self.store_list])

    def setup(self):
        self.set_store_points()
        self.set_boundaries()

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
        return ConsellationFinder.haversine(lon1, lat1, lon2, lat2)

    def find_store_near_coordinates(self, coordinates):
        if coordinates[0] < -180 or coordinates[0] > 180:
            return
        if coordinates[1] < -90 or coordinates[1] > 90:
            return
        distance, point = self.store_kd_tree.get_nearest(coordinates)
        if self.haversine_from_points(point, coordinates) <= self.ACCEPTABLE_DISTANCE:
            return point

    def get_store_near_coordinates(self, coordinates) -> typing.Optional[StorePoint]:
        distance, point = self.store_kd_tree.get_nearest(coordinates)
        if ConsellationFinder.haversine_from_points(point, coordinates) <= ConsellationFinder.ACCEPTABLE_DISTANCE:
            return point

    def examine_location_permutation(self, list_of_stores):
        location_1, location_2 = list_of_stores[0], list_of_stores[1]
        scaled_constellation = get_projected_constellation(location_1, location_2, self.constellation_points)
        stores_in_constellation = [location_1, location_2]
        for next_location in scaled_constellation[2:]:
            store_in_constellation = self.find_store_near_coordinates(next_location)
            if store_in_constellation is None:
                return
            stores_in_constellation.append(store_in_constellation)
        return stores_in_constellation

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

    def get_consellation(self, store_point_1: StorePoint, store_point_2: StorePoint):
        projected_constellation = get_projected_constellation(store_point_1, store_point_2, self.constellation_points)

        #   Validate constellation is within boundary.
        if min([c[0] for c in projected_constellation]) < self.x_min:
            self.boundary_fails += 1
            return
        if max([c[0] for c in projected_constellation]) > self.x_max:
            self.boundary_fails += 1
            return
        if min([c[1] for c in projected_constellation]) < self.y_min:
            self.boundary_fails += 1
            return
        if max([c[1] for c in projected_constellation]) > self.y_max:
            self.boundary_fails += 1
            return

        return self.get_recursive_constellation(projected_constellation, [])

    def write_consellation(self, consellation_points):
        with open('points.txt', 'a') as record:
            record.write('%s,%s\n' % (
                self.constellation_name,
                ','.join([x.get_store_id() for x in consellation_points])
            ))

    def run(self):
        self.setup()
        permutations_checked = 0
        start_time = time.time()
        for i, store_1 in enumerate(self.store_list):
            for store_2 in self.store_list[i + 1:]:
                #   distance = self.haversine_from_points(store_1, store_2)
                result = self.get_consellation(store_1, store_2)
                if result is not None:
                    print('const points =', [x.get_point() for x in result])
                    self.write_consellation(result)
                permutations_checked += 1
                if permutations_checked % 1000000 == 0:
                    print('Checked %s combinations' % permutations_checked)
                    print('Took %s seconds' % (time.time() - start_time))
                    start_time = time.time()
            self.boundary_fails = 0


