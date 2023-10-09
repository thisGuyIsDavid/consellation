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