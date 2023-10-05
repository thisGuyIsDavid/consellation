from app.db import get_all_rows

def get_points(uuid: str):
    points = get_all_rows(
        """
        SELECT CF.store_id, latitude, longitude 
        FROM cf_constellations_found CF
        JOIN store_list
            ON store_list.id = CF.store_id
        WHERE constellation_uuid= %(uuid)s
        """, {
            'uuid': uuid
        }
    )
    print(points)

get_points('ad9a733c-5246-4a5f-bf75-77fb81901200')