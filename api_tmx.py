#!/usr/bin/env python3

import requests
import json
import logging

from api_strategy import ApiStrategy
from api_exc import RateLimitException
from datetime import datetime
from repositories import RepositoryFactory

from models import APIMeta

# 1 request every 2 minutes
# XXX: Last request is saved on DB as int, which means fastest requests happen
# every second. This is not bad, as we also don't want to overload servers,
# so I won't "fix" it.
G_RATE_LIMIT = 80.0


class ApiTmxStrategy(ApiStrategy):
    def __init__(self, repoFactory: RepositoryFactory):
        repoMeta = repoFactory.getAPIMetaRepo()
        meta = repoMeta.getMeta()

        self._g_tmx_url = "https://trackmania.exchange"
        self._g_tmio_url = "https://trackmania.io"
        self._headers = {
            "User-Agent": "StreamerRMCNotifier / ricardojorge512@hotmail.com"
        }
        self._meta: APIMeta = meta

    def _check_rate_limit(self):
        if not self._meta.lastRequestTimestamp:
            self._meta.lastRequestTimestamp = int(datetime.now().timestamp())
            return

        curr_t = int(datetime.now().timestamp())
        delta = float(curr_t - self._meta.lastRequestTimestamp)

        if delta < G_RATE_LIMIT:
            twait = G_RATE_LIMIT - delta + 0.5
            raise RateLimitException(f"Rated limited for {twait} seconds.",
                                     twait)

        self._meta.lastRequestTimestamp = curr_t

    def search_maps(self, authorid, limit, page):
        params = {
            "api": "on",
            "authorid": authorid,
            "limit": limit,
            "page": page
        }
        headers = self._headers
        self._check_rate_limit()
        url = f"{self._g_tmx_url}/mapsearch2/search"
        logging.debug("> GET")
        logging.debug(f"> URL: {url}")
        logging.debug(f"> params: {json.dumps(params, default='str')}")
        logging.debug(f"> headers: {json.dumps(headers, default='str')}")
        res = requests.get(url, params=params, headers=headers)
        logging.debug(f"> Response: {res.status_code}")
        if res.status_code // 100 != 2:
            logging.debug(f"> Body: {res.content}")
            raise RuntimeError("Failed to query maps for authorid: " +
                               f"{authorid}")
        result = json.loads(res.content)
        logging.debug(f"> Body: {json.dumps(result, indent=4, default='str')}")
        return result

    def get_offline_records(self, trackid):
        self._check_rate_limit()
        headers = self._headers
        url = f"{self._g_tmx_url}/api/replays/get_replays/{trackid}"
        logging.debug("> GET")
        logging.debug(f"> URL: {url}")
        logging.debug(f"> headers: {json.dumps(headers, default='str')}")
        res = requests.get(url, headers=headers)
        logging.debug(f"> Response: {res.status_code}")
        if res.status_code // 100 != 2:
            logging.debug(f"> Body: {res.content}")
            raise RuntimeError("Failed to query records for trackid: " +
                               f"{trackid}")
        result = json.loads(res.content)
        logging.debug(f"> Body: {json.dumps(result, indent=4, default='str')}")
        return result

    def get_online_records(self, trackuid, offset, length):
        self._check_rate_limit()
        params = {
            "offset": offset,
            "length": length
        }
        headers = self._headers
        url = f"{self._g_tmio_url}/api/leaderboard/map/{trackuid}"
        logging.debug("> GET")
        logging.debug(f"> URL: {url}")
        logging.debug(f"> params: {json.dumps(params, default='str')}")
        logging.debug(f"> headers: {json.dumps(headers, default='str')}")
        res = requests.get(url, params=params, headers=headers)
        logging.debug(f"> Response: {res.status_code}")
        if res.status_code // 100 != 2:
            logging.debug(f"> Body: {res.content}")
            raise RuntimeError("Failed to query online records for " +
                               f"trackuid: {trackuid}")
        result = json.loads(res.content)
        logging.debug(f"> Body: {json.dumps(result, indent=4, default='str')}")
        return result


if __name__ == "__main__":
    pass
