from app.db import get_all_rows, get_row, insert
import os


class StorePoint:

    def __init__(self, **kwargs):
        self.store_id = kwargs.get('store_id')
        self.x = kwargs.get('longitude')
        self.y = kwargs.get('latitude')

    def __getitem__(self, key):
        return [self.x, self.y][key]

    def __str__(self):
        return f"Point {self.store_id} ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.store_id

    def get_point(self):
        return [self.x, self.y]

    def get_store_id(self) -> str:
        return str(self.store_id)

    def set_as_processed(self):
        insert(
            """
            INSERT INTO cf_stores_checked (
                store_id, checker_name
            ) VALUES (
                %(store_id)s, %(checker_name)s
            )
            """, {
                'store_id': self.get_store_id(),
                'checker_name': os.getenv('PROCESSOR_NAME')
            }
        )

    @staticmethod
    def get_stores(company_name):
        response = get_all_rows(
            """
            SELECT id AS store_id, latitude, longitude
            FROM store_list
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            AND id != 676778
            AND company_name = %(company_name)s
            AND country_code = 'US'
            AND TRIM(state_alpha) NOT IN ('AK', 'HI')
            AND longitude < 0 AND latitude > 0
            ORDER BY id
            """, {'company_name': company_name}
        )
        return [StorePoint(**x) for x in response]

    @staticmethod
    def get_store(company_name):
        response = get_row(
            """
            SELECT id AS store_id, latitude, longitude
            FROM store_list
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            AND country_code = 'US'
            AND company_name = %(company_name)s
            AND id NOT IN (SELECT store_id FROM cf_stores_checked)
            ORDER BY RAND()
            LIMIT 1
            """, {'company_name': company_name}
        )
        return StorePoint(**response)