import math


def get_angle(point_1, point_2):
    x = point_2[0] - point_1[0]
    y = point_2[1] - point_1[1]
    theta = math.atan2(y, x)
    return math.degrees(theta)


def rotate_along_point(coordinates, angle):
    x,y = coordinates
    angler = angle*math.pi/180
    new_x = x*math.cos(angler) - y*math.sin(angler)
    new_y = x*math.sin(angler) + y*math.cos(angler)
    return new_x, new_y


def get_angle_to_rotate(store_angle, constellation_angle):
    return store_angle - constellation_angle


def get_rotated_constellation(constellation, location_1, location_2):
    angle_of_locations = get_angle(location_1, location_2)
    angle_of_constellation = get_angle(constellation[0], constellation[1])
    angle_to_rotate = get_angle_to_rotate(angle_of_locations, angle_of_constellation)
    return [rotate_along_point((point[0], point[1]), angle_to_rotate) for point in constellation]


def scale(coordinates, scale_factor):
    x, y = coordinates
    scaled_x = x * scale_factor
    scaled_y = y * scale_factor
    return scaled_x, scaled_y


def get_shifted_constellation(constellation, location_1):
    shift_x = (constellation[0][0] - location_1[0])
    shift_y = (constellation[0][1] - location_1[1])
    return [[point[0] - shift_x, point[1] - shift_y] for point in constellation]


def get_scaled_constellation(constellation, location_1, location_2):
    distance_between_locations = math.dist(location_1, location_2)
    distance_between_constellation = math.dist(constellation[0], constellation[1])
    scaled_size = distance_between_locations / distance_between_constellation
    scaled_constellation = [scale(x, scaled_size) for x in constellation]
    return scaled_constellation


def get_projected_constellation(point_1, point_2, constellation):
    constellation = get_rotated_constellation(constellation, point_1, point_2)
    constellation = get_scaled_constellation(constellation, point_1, point_2)
    constellation = get_shifted_constellation(constellation, point_1)
    return constellation


"""
    def run_audit(self):
# make the data
x = [x[0] for x in scaled_constellation]
y = [x[1] for x in scaled_constellation]

#   assert points for location one match.
assert round(x[0], 6) == round(location_1[0], 6)
assert round(y[0], 6) == round(location_1[1], 6)

if round(x[1], 5) != round(location_2[0], 5) or round(y[1], 5) != round(location_2[1], 5):
    print('DISTANCE %s vs. %s' % (
        math.dist(scaled_constellation[0], scaled_constellation[1]),
        math.dist(location_1, location_2)
    ))
    print('ANGLE %s vs. %s' % (
        self.get_angle(scaled_constellation[0], scaled_constellation[1]),
        self.get_angle(location_1, location_2)
    ))

    raise AssertionError

:return:
"""