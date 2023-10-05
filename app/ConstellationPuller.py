from app.db import get_all_rows
from app.constellation.StorePoint import StorePoint
from app.constellation.ConstellationFinder import ConstellationFinder

def get_points(uuid: str):
    points = get_all_rows(
        """
        SELECT constellation_name, CF.store_id, latitude, longitude 
        FROM cf_constellations_found CF
        JOIN store_list
            ON store_list.id = CF.store_id
        WHERE constellation_uuid= %(uuid)s
        """, {
            'uuid': uuid
        }
    )
    return [StorePoint(**x) for x in points]

points = get_points('ad9a733c-5246-4a5f-bf75-77fb81901200')

max_x = max([p.x for p in points])
max_y = max([p.y for p in points])
min_x = min([p.x for p in points])
min_y = min([p.y for p in points])

distance = ConstellationFinder.haversine(
    max_x, max_y, min_x, min_y
)
print(distance)


