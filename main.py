from app.constellation.Constellation import Constellation
from app.constellation.ConstellationsFinder import ConstellationsFinder
from app.constellation.KDTree import KDTree
from app.constellation.StorePoint import StorePoint
import random

companies = [
    'Starbucks', 'Burger King', 'Wendys', 'Target', 'Taco Bell', 'Subway', 'McDonalds', 'Dunkin',
    'Denny\'s', 'Culvers', 'Arbys', 'Chipotle'
]
company_to_check = companies[random.randint(0, len(companies) - 1)]
print('Checking', company_to_check)

store_list = StorePoint.get_stores(company_name=company_to_check)
store_lookup = KDTree(store_list, dim=2)
constellations = Constellation.get_constellations()
store_to_examine = StorePoint.get_store(company_name=company_to_check)
while store_to_examine is not None:
    ConstellationsFinder(
        store_to_examine=store_to_examine,
        constellations=constellations,
        store_list=store_list,
        store_lookup=store_lookup
    ).run()
    store_to_examine = StorePoint.get_store(company_name=company_to_check)