from bs4 import BeautifulSoup

crown = [[1.9, 21.53], [11.72, 55.42], [32.62, 64.92], [51.62, 61.75], [72.52, 54.79], [73.79, 1.58], [87.72, 26.28]]
orion = [[8.28, 97.85], [16.25, 98.47], [1.53, 78.85], [5.21, 80.69], [9.5, 65.36], [30.97, 65.36], [15.02, 59.22], [37.71, 54.93], [32.8, 34.7], [28.51, 31.63], [25.45, 28.57], [19.93, 5.26], [45.68, 9.56], [59.17, 77.01], [64.69, 63.52], [65.3, 56.16], [64.08, 51.25], [62.24, 42.67], [57.94, 39.6]]
taurus = [[2.18, 82.97], [23.14, 97.82], [41.47, 64.64], [46.71, 50.67], [48.46, 42.81], [79.02, 48.92], [40.6, 38.45], [34.49, 47.18], [56.32, 19.24], [46.71, 34.95], [78.14, 10.51]]

def get_coordinates_from_svg():
    svg_text = open('con.svg').read()
    soup = BeautifulSoup(svg_text, features='xml')
    coordinates = []
    for circle in soup.find_all('circle'):
        x = float(circle.get('cx'))
        y = 100 - float(circle.get('cy'))
        print(x, y)
        coordinates.append([round(x, 3), round(y, 3)])
    return coordinates

print(get_coordinates_from_svg())