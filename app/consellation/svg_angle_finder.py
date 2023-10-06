from bs4 import BeautifulSoup


def get_coordinates_from_svg():
    svg_text = open('con.svg').read()
    soup = BeautifulSoup(svg_text, features='xml')
    coordinates = []
    for circle in soup.find_all('circle'):
        x = float(circle.get('cx'))
        y = 100 - float(circle.get('cy'))
        coordinates.append([round(x, 3), round(y, 3)])
    return coordinates

print(get_coordinates_from_svg())