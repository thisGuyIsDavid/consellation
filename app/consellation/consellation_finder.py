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

    def get_point(self):
        return [self.x, self.y]


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

    def __init__(self, constellation_points):
        self.store_list: typing.List[StorePoint] = []
        self.store_kd_tree: typing.Optional[KDTree] = None
        self.constellation_points: list = constellation_points

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

    def set_k_d_tree(self, store_list):
        start = time.time()
        self.store_kd_tree = KDTree(store_list, dim=2)
        print('KD Tree build took %s seconds' % (time.time() - start))

    def setup(self):
        self.set_store_points()
        self.set_k_d_tree(self.store_list)

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

    @staticmethod
    def get_store_near_coordinates(coordinates, store_list) -> typing.Optional[StorePoint]:
        if coordinates[0] < -180 or coordinates[0] > 180:
            return
        if coordinates[1] < -90 or coordinates[1] > 90:
            return
        distance, point = KDTree(store_list, dim=2).get_nearest(coordinates)
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
        closest_store = ConsellationFinder.get_store_near_coordinates(point_to_check, store_list)
        if closest_store is None:
            return
        store_list = [x for x in store_list if x.store_id != closest_store.store_id]
        stores_in_constellation.append(closest_store)
        if len(stores_in_constellation) == len(projected_constellation):
            return stores_in_constellation
        return self.get_recursive_constellation(projected_constellation, store_list, stores_in_constellation)

    def get_consellation(self, store_point_1: StorePoint, store_point_2: StorePoint):
        projected_constellation = get_projected_constellation(store_point_1, store_point_2, self.constellation_points)
        return self.get_recursive_constellation(projected_constellation, self.store_list, [])

    def run(self):
        self.setup()
        permutations_checked = 0
        for store_permutation in permutations(self.store_list, 2):
            print(store_permutation)
            result = self.get_consellation(store_permutation[0], store_permutation[1])
            if result is not None:
                print('const points =', [x.get_point() for x in result])
            print(result)
            permutations_checked += 1
            if permutations_checked % 100000 == 0:
                print('Checked %s combinations' % permutations_checked)

if __name__ == '__main__':
    line = [[0,0], [0,5], [0, 10]]
    crown = [[1.9, 21.53], [11.72, 55.42], [32.62, 64.92], [51.62, 61.75], [72.52, 54.79], [73.79, 1.58], [87.72, 26.28]]
    orion = [[8.28, 97.85], [16.25, 98.47], [1.53, 78.85], [5.21, 80.69], [9.5, 65.36], [30.97, 65.36], [15.02, 59.22], [37.71, 54.93], [32.8, 34.7], [28.51, 31.63], [25.45, 28.57], [19.93, 5.26], [45.68, 9.56], [59.17, 77.01], [64.69, 63.52], [65.3, 56.16], [64.08, 51.25], [62.24, 42.67], [57.94, 39.6]]
    taurus = [[2.18, 82.97], [23.14, 97.82], [41.47, 64.64], [46.71, 50.67], [48.46, 42.81], [79.02, 48.92], [40.6, 38.45], [34.49, 47.18], [56.32, 19.24], [46.71, 34.95], [78.14, 10.51]]
    ursa_minor = [[38.5, 97.5], [25.5, 70.5], [11.5, 36.5], [21.5, 0.5], [43.5, -30.5], [2.5, -11.5], [25.5, -47.5]]
    ursa_major = [[2.5, 71.5], [21.5, 80.5], [68.5, 2.5], [34.5, 80.5], [56.5, 46.5], [50.5, 76.5], [56.5, 64.5], [75.5, 35.5], [102.5, 27.5], [78.5, 85.5], [79.5, 70.5], [136.5, 54.5], [109.5, 94.5], [106.5, 81.5], [118.5, 62.5], [132.5, 97.5]]
    lyra = [[37.5, 97.5], [36.5, 74.5], [54.5, 88.5], [14.5, 63.5], [25.5, 22.5], [2.5, 16.5]]
    leo_minor = [[4.5, 75.5], [125.5, 95.5], [45.5, 91.5], [73.5, 82.5], [47.5, 71.5]]
    leo = [[4.5, 40.5], [151.5, 17.5], [94.5, 11.5], [118.5, 27.5], [34.5, -1.5], [31.5, 20.5], [42.5, 43.5], [44.5, 67.5], [106.5, 63.5], [120.5, 50.5], [109.5, 81.5], [142.5, 82.5], [134.5, 94.5], [159.5, 80.5], [165.5, 95.5]]
    hercules = [[12.5, 96.5], [10.5, 76.5], [20.5, 68.5], [36.5, 27.5], [3.5, -21.5], [52.5, 32.5], [16.5, -29.5], [41.5, -1.5], [26.5, -34.5], [34.5, -17.5], [64.5, 57.5], [65.5, 9.5], [74.5, 7.5], [102.5, 7.5], [85.5, -29.5], [80.5, 52.5], [93.5, 46.5], [103.5, 39.5], [114.5, 42.5]]

    constellations = [
        ['Line', line],
        ['Crown', crown],
        ['Ursa Major', ursa_major],
        ['Hercules', hercules],
        ['Leo Minor', leo_minor],
        ['Orion', orion],
        ['Taurus', taurus],
        ['Ursa Minor', ursa_minor],
        ['Lyra', lyra],
        ['Leo', leo]
    ]

    for constellation_to_check in constellations:
        title, constellation = constellation_to_check
        ConsellationFinder(constellation_points=constellation).run()
