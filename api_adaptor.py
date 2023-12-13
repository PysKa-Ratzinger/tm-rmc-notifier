#!/usr/bin/env python3

from api_mockup import ApiMockupStrategy
from api_tmx import ApiTmxStrategy
from api_strategy import ApiStrategy

from repositories import RepositoryFactory


class ApiAdaptor:
    def __init__(self, strategy: ApiStrategy):
        self._strategy = strategy

    def search_maps(self, authorid, limit, page):
        return self._strategy.search_maps(authorid, limit, page)

    def get_offline_records(self, trackid):
        return self._strategy.get_offline_records(trackid)

    def get_online_records(self, trackuid, offset, length):
        return self._strategy.get_online_records(trackuid, offset, length)


def get_adaptor(test_api: bool, repoFactory: RepositoryFactory):
    if test_api:
        return ApiAdaptor(ApiMockupStrategy())
    else:
        return ApiAdaptor(ApiTmxStrategy(repoFactory))


if __name__ == "__main__":
    pass
