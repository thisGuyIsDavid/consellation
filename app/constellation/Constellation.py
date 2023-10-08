import math
import typing


class Constellation:

    def __init__(self, name:str, points: typing.List):
        self.name = name
        self.points: typing.List = points

    @staticmethod
    def get_angle(point_1, point_2):
        x = point_2[0] - point_1[0]
        y = point_2[1] - point_1[1]
        theta = math.atan2(y, x)
        return math.degrees(theta)

    @staticmethod
    def rotate_along_point(coordinates, angle):
        x, y = coordinates
        angler = angle*math.pi/180
        new_x = x*math.cos(angler) - y*math.sin(angler)
        new_y = x*math.sin(angler) + y*math.cos(angler)
        return new_x, new_y

    @staticmethod
    def get_angle_to_rotate(store_angle, constellation_angle):
        return store_angle - constellation_angle

    @staticmethod
    def get_rotated_constellation(constellation, location_1, location_2):
        angle_of_locations = Constellation.get_angle(location_1, location_2)
        angle_of_constellation = Constellation.get_angle(constellation[0], constellation[1])
        angle_to_rotate = Constellation.get_angle_to_rotate(angle_of_locations, angle_of_constellation)
        return [Constellation.rotate_along_point((point[0], point[1]), angle_to_rotate) for point in constellation]

    @staticmethod
    def scale(coordinates, scale_factor):
        x, y = coordinates
        scaled_x = x * scale_factor
        scaled_y = y * scale_factor
        return scaled_x, scaled_y

    @staticmethod
    def get_shifted_constellation(constellation, location_1):
        shift_x = (constellation[0][0] - location_1[0])
        shift_y = (constellation[0][1] - location_1[1])
        return [[point[0] - shift_x, point[1] - shift_y] for point in constellation]

    @staticmethod
    def get_scaled_constellation(constellation, location_1, location_2):
        distance_between_locations = math.dist(location_1, location_2)
        distance_between_constellation = math.dist(constellation[0], constellation[1])
        scaled_size = distance_between_locations / distance_between_constellation
        scaled_constellation = [Constellation.scale(x, scaled_size) for x in constellation]
        return scaled_constellation

    def get_projected_constellation(self, point_1, point_2):
        constellation = self.get_rotated_constellation(self.points, point_1, point_2)
        constellation = self.get_scaled_constellation(constellation, point_1, point_2)
        constellation = self.get_shifted_constellation(constellation, point_1)
        return constellation

    @staticmethod
    def get_constellations():
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
            ['Aries', [[2.0, 98.0], [84.0, 77.0], [119.0, 59.0], [124.0, 40.0]]],
            ['Gemini', [[17.0, 98.0], [26.0, 96.0], [40.0, 94.0], [2.0, 74.0], [6.0, 59.0], [31.0, 49.0], [52.0, 43.0], [80.0, 71.0], [105.0, 62.0], [117.0, 61.0], [100.0, 46.0], [90.0, 27.0], [83.0, 5.0]]],
            ['Cancer', [[2.0, 98.0], [26.0, 67.0], [31.0, 54.0], [91.0, 32.0], [29.0, 14.0]]],
            ['Leo', [[101.0, 94.0], [88.0, 98.0], [73.0, 77.0], [76.0, 61.0], [93.0, 53.0], [99.0, 34.0], [31.0, 19.0], [24.0, 43.0], [2.0, 9.0]]],
            ['Virgo', [[2.0, 40.0], [30.0, 52.0], [16.0, 14.0], [34.0, 21.0], [51.0, 55.0], [41.0, 15.0], [70.0, 26.0], [72.0, 48.0], [54.0, 98.0], [70.0, 79.0], [85.0, 72.0], [101.0, 80.0], [110.0, 92.0]]],
            ['Taurus', [[18.0, 98.0], [2.0, 69.0], [43.0, 71.0], [45.0, 42.0], [52.0, 55.0], [53.0, 48.0], [59.0, 48.0], [54.0, 39.0], [61.0, 39.0], [76.0, 28.0], [111.0, 15.0], [113.0, 8.0]]],
            ['Libra', [[19.0, 60.0], [12.0, 45.0], [2.0, 32.0], [17.0, 98.0], [65.0, 85.0], [80.0, 38.0], [58.0, 6.0], [65.0, -6.0]]],
            ['Scorpius', [[103.0, 98.0], [106.0, 87.0], [75.0, 75.0], [84.0, 79.0], [105.0, 75.0], [69.0, 69.0], [104.0, 62.0], [55.0, 49.0], [52.0, 32.0], [47.0, 16.0], [31.0, 14.0], [12.0, 15.0], [2.0, 27.0], [8.0, 33.0], [16.0, 40.0]]],
            ['Sagittarius', [[26.0, 98.0], [40.0, 89.0], [50.0, 88.0], [58.0, 91.0], [58.0, 68.0], [69.0, 64.0], [50.0, 61.0], [56.0, 54.0], [23.0, 67.0], [7.0, 50.0], [2.0, 44.0], [20.0, 17.0], [30.0, -1.0], [46.0, 7.0], [52.0, -6.0], [91.0, 38.0], [98.0, 31.0], [87.0, 71.0], [94.0, 55.0], [108.0, 53.0], [96.0, 93.0], [128.0, 66.0]]],
            ['Capricorn', [[10.0, 31.0], [2.0, 24.0], [19.0, 20.0], [27.0, 39.0], [44.0, 46.0], [36.0, 15.0], [58.0, 17.0], [76.0, 16.0], [79.0, 23.0], [90.0, 85.0], [93.0, 98.0]]],
            ['Aquarius', [[39.0, 79.0], [66.0, 98.0], [10.0, 61.0], [34.0, 47.0], [53.0, 51.0], [10.0, 45.0], [3.0, 43.0], [2.0, 36.0], [27.0, 21.0], [22.0, 7.0], [43.0, 24.0], [48.0, 19.0], [60.0, 11.0]]],
            ['Pisces', [[2.0, 0.0], [20.0, 2.0], [12.0, -5.0], [45.0, 3.0], [65.0, 2.0], [84.0, -3.0], [58.0, 27.0], [72.0, 10.0], [53.0, 38.0], [42.0, 65.0], [38.0, 79.0], [33.0, 86.0], [34.0, 95.0], [41.0, 98.0], [50.0, 95.0], [51.0, 84.0], [48.0, 77.0]]],
        ]
        constellation_list = []
        for constellation in constellations:
            constellation_list.append(Constellation(constellation[0], constellation[1]))
        return constellation_list