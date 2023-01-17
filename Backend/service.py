
from repo import Repo


class Service:


    @classmethod
    def optimize(cls, defaulth,num ,changed_values, indicator):
        return Repo().optimize(defaulth, num, changed_values, indicator)