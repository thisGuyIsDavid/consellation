from app.consellation.consellation_finder import ConsellationFinder

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
        #   ['Line', line],
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
