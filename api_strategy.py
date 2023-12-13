#!/usr/bin/env python3

from abc import ABC, abstractmethod


class ApiStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def search_maps(self, authorid, limit, page):
        pass

    @abstractmethod
    def get_offline_records(self, trackid):
        pass

    @abstractmethod
    def get_online_records(self, trackuid, offset, length):
        pass


if __name__ == "__main__":
    pass
