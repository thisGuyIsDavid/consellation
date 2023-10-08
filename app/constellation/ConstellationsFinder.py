import typing

from app.constellation.Constellation import Constellation
from app.constellation.ConstellationFinder import ConstellationFinder
from app.constellation.KDTree import KDTree
from app.constellation.StorePoint import StorePoint


class ConstellationsFinder:

    def __init__(self,
                 store_to_examine: StorePoint,
                 constellations: typing.List[Constellation],
                 store_list: typing.List[StorePoint],
                 store_lookup: KDTree
    ):
        self.store_to_examine: StorePoint = store_to_examine
        self.constellations: typing.List[Constellation] = constellations
        self.store_list: typing.List[StorePoint] = store_list
        self.store_lookup: KDTree = store_lookup

    def process_constellation(self, constellation: Constellation):
        minimum_constellation_size = 250
        for store_to_test in self.store_list:
            #   Don't check a store against itself.
            if store_to_test.store_id == self.store_to_examine.store_id:
                continue
            discovered_constellation = ConstellationFinder(
                point_1=self.store_to_examine,
                point_2=store_to_test,
                constellation=constellation,
                minimum_constellation_size=minimum_constellation_size,
                store_lookup=self.store_lookup
            ).process()
            if discovered_constellation is None:
                continue
            minimum_constellation_size = discovered_constellation

    def run(self):
        for constellation in self.constellations:
            self.process_constellation(constellation)
        self.store_to_examine.set_as_processed()

