

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

    @staticmethod
    def get_stores():
        response = []
        with open('store.txt', 'r') as raw_stores:
            for line in raw_stores:
                split_line = line.split(',')
                response.append({
                    'store_id': int(split_line[0]),
                    'latitude': float(split_line[1]),
                    'longitude': float(split_line[2])
                })

        return [StorePoint(**x) for x in response]