import time
import typing
from itertools import permutations
from math import radians, cos, sin, asin, sqrt

from app.consellation.constellation_utils import get_projected_constellation


class StorePoint:

    def __init__(self, **kwargs):
        self.store_id = kwargs.get('store_id')
        self.x = kwargs.get('longitude')
        self.y = kwargs.get('latitude')

    def __getitem__(self, key):
        return [self.x, self.y][key]

    def __str__(self):
        return f"Point {self.store_id} ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.store_id

    def get_point(self):
        return [self.x, self.y]

    def get_store_id(self) -> str:
        return str(self.store_id)


class KDTree(object):

    """
    A super short KD-Tree for points...
    so concise that you can copypasta into your homework
    without arousing suspicion.

    This implementation only supports Euclidean distance.

    The points can be any array-like type, e.g:
        lists, tuples, numpy arrays.

    Usage:
    1. Make the KD-Tree:
        `kd_tree = KDTree(points, dim)`
    2. You can then use `get_knn` for k nearest neighbors or
       `get_nearest` for the nearest neighbor

    points are be a list of points: [[0, 1, 2], [12.3, 4.5, 2.3], ...]
    """
    def __init__(self, points, dim, dist_sq_func=None):
        """Makes the KD-Tree for fast lookup.

        Parameters
        ----------
        points : list<point>
            A list of points.
        dim : int
            The dimension of the points.
        dist_sq_func : function(point, point), optional
            A function that returns the squared Euclidean distance
            between the two points.
            If omitted, it uses the default implementation.
        """

        if dist_sq_func is None:
            dist_sq_func = lambda a, b: sum((x - b[i]) ** 2 for i, x in enumerate(a))

        def make(points, i=0):
            if len(points) > 1:
                points.sort(key=lambda x: x[i])
                i = (i + 1) % dim
                m = len(points) >> 1
                return [make(points[:m], i), make(points[m + 1:], i),
                        points[m]]
            if len(points) == 1:
                return [None, None, points[0]]

        def add_point(node, point, i=0):
            if node is not None:
                dx = node[2][i] - point[i]
                for j, c in ((0, dx >= 0), (1, dx < 0)):
                    if c and node[j] is None:
                        node[j] = [None, None, point]
                    elif c:
                        add_point(node[j], point, (i + 1) % dim)

        import heapq
        def get_knn(node, point, k, return_dist_sq, heap, i=0, tiebreaker=1):
            if node is not None:
                dist_sq = dist_sq_func(point, node[2])
                dx = node[2][i] - point[i]
                if len(heap) < k:
                    heapq.heappush(heap, (-dist_sq, tiebreaker, node[2]))
                elif dist_sq < -heap[0][0]:
                    heapq.heappushpop(heap, (-dist_sq, tiebreaker, node[2]))
                i = (i + 1) % dim
                # Goes into the left branch, then the right branch if needed
                for b in (dx < 0, dx >= 0)[:1 + (dx * dx < -heap[0][0])]:
                    get_knn(node[b], point, k, return_dist_sq,
                            heap, i, (tiebreaker << 1) | b)
            if tiebreaker == 1:
                return [(-h[0], h[2]) if return_dist_sq else h[2]
                        for h in sorted(heap)][::-1]

        def walk(node):
            if node is not None:
                for j in 0, 1:
                    for x in walk(node[j]):
                        yield x
                yield node[2]

        self._add_point = add_point
        self._get_knn = get_knn
        self._root = make(points)
        self._walk = walk

    def __iter__(self):
        return self._walk(self._root)

    def add_point(self, point):
        """Adds a point to the kd-tree.

        Parameters
        ----------
        point : array-like
            The point.
        """
        if self._root is None:
            self._root = [None, None, point]
        else:
            self._add_point(self._root, point)

    def get_knn(self, point, k, return_dist_sq=True):
        """Returns k nearest neighbors.

        Parameters
        ----------
        point : array-like
            The point.
        k: int
            The number of nearest neighbors.
        return_dist_sq : boolean
            Whether to return the squared Euclidean distances.

        Returns
        -------
        list<array-like>
            The nearest neighbors.
            If `return_dist_sq` is true, the return will be:
                [(dist_sq, point), ...]
            else:
                [point, ...]
        """
        return self._get_knn(self._root, point, k, return_dist_sq, [])

    def get_nearest(self, point, return_dist_sq=True):
        """Returns the nearest neighbor.

        Parameters
        ----------
        point : array-like
            The point.
        return_dist_sq : boolean
            Whether to return the squared Euclidean distance.

        Returns
        -------
        array-like
            The nearest neighbor.
            If the tree is empty, returns `None`.
            If `return_dist_sq` is true, the return will be:
                (dist_sq, point)
            else:
                point
        """
        l = self._get_knn(self._root, point, 1, return_dist_sq, [])
        return l[0] if len(l) else None


class ConsellationFinder:

    ACCEPTABLE_DISTANCE = 10

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
        response = []
        with open('store.txt', 'r') as raw_stores:
            for line in raw_stores:
                split_line = line.split(',')
                response.append({
                    'store_id': int(split_line[0]),
                    'latitude': float(split_line[1]),
                    'longitude': float(split_line[2])
                })
        self.store_list = [StorePoint(**x) for x in response]
        self.store_kd_tree = KDTree(self.store_list, dim=2)

    def set_boundaries(self):
        self.x_min = min([s.x for s in self.store_list])
        self.x_max = max([s.x for s in self.store_list])
        self.y_min = min([s.y for s in self.store_list])
        self.y_max = max([s.y for s in self.store_list])

    def setup(self):
        self.set_store_points()
        self.set_boundaries()
        print('Set')

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

    def get_store_near_coordinates(self, coordinates, store_list) -> typing.Optional[StorePoint]:
        if coordinates[0] < -180 or coordinates[0] > 180:
            return
        if coordinates[1] < -90 or coordinates[1] > 90:
            return
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

    def get_recursive_constellation(self, projected_constellation, store_list, stores_in_constellation: typing.List):
        point_to_check = projected_constellation[len(stores_in_constellation)]
        closest_store = self.get_store_near_coordinates(point_to_check, store_list)
        if closest_store is None:
            return
        stores_in_constellation.append(closest_store)
        if len(stores_in_constellation) == len(projected_constellation):
            if len(set(stores_in_constellation)) == len(stores_in_constellation):
                return stores_in_constellation
            else:
                return
        return self.get_recursive_constellation(projected_constellation, store_list, stores_in_constellation)

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

        return self.get_recursive_constellation(projected_constellation, self.store_list, [])

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
            print(i, self.boundary_fails)
            self.boundary_fails = 0

