from app.db import insert_many, insert
import uuid
import os

store_ids_found = []
constellations_found = []

with open('points.txt') as raw_points:
    for line in raw_points:
        stripped_line = line.strip()
        split_line = stripped_line.split(',')
        constellation_name = split_line[0]
        store_ids = split_line[1:]

        constellations_found.append({
            'constellation_name': constellation_name,
            'constellation_string': '|'.join(store_ids),
        })
        store_ids_found.append(store_ids[0])
        continue
        constellation_id = uuid.uuid4()
        insert(
            """
            INSERT INTO cf_raw_constellations (
                constellation_name, constellation_string, when_created
            ) VALUES (
                %(constellation_name)s,  %(constellation_string)s, CURRENT_TIMESTAMP
            )
            """,
            {
                'constellation_name': constellation_name,
                'constellation_string': '|'.join(store_ids),
            }
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


for i in range(490):
    cf = constellations_found[i * 100: (i + 1) * 100]
    insert_many(
        """
        INSERT INTO cf_raw_constellations (
            constellation_name, constellation_string, when_created
        ) VALUES (
            %(constellation_name)s,  %(constellation_string)s, CURRENT_TIMESTAMP
        )
        """,
        cf
    )

print(len(set(store_ids_found)))
print(len(constellations_found))