from app.db import insert_many, insert
import uuid
import os

with open('points.txt') as raw_points:
    for line in raw_points:
        stripped_line = line.strip()
        split_line = stripped_line.split(',')
        constellation_name = split_line[0]
        store_ids = split_line[1:]

        constellation_id = uuid.uuid4()
        insert_many(
            """
            INSERT INTO cf_constellations_found (
                constellation_name, constellation_uuid, store_id, when_created
            ) VALUES (
                %(constellation_name)s, %(constellation_uuid)s, %(store_id)s, CURRENT_TIMESTAMP
            )
            """, [
                {
                    'constellation_name': constellation_name,
                    'constellation_uuid': constellation_id,
                    'store_id': x
                } for x in store_ids
            ]
        )
        insert(
            """
            INSERT IGNORE INTO cf_stores_checked (
                store_id, checker_name
            ) VALUES (
                %(store_id)s, %(checker_name)s
            )
            """, {
                'store_id': store_ids[0],
                'checker_name': os.getenv('PROCESSOR_NAME')
            }
        )