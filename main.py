from app.constellation.Constellation import Constellation
from app.constellation.ConstellationsFinder import ConstellationsFinder
from app.constellation.KDTree import KDTree
from app.constellation.StorePoint import StorePoint

store_list = StorePoint.get_stores()
store_lookup = KDTree(store_list, dim=2)
constellations = Constellation.get_constellations()
store_to_examine = StorePoint.get_store()
while store_to_examine is not None:
    ConstellationsFinder(
        store_to_examine=store_to_examine,
        constellations=constellations,
        store_list=store_list,
        store_lookup=store_lookup
    ).run()
    store_to_examine = StorePoint.get_store()