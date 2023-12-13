#!/usr/bin/env python3

import logging

from repositories import RepositoryFactory
from api_adaptor import ApiAdaptor
from models import TMXMap, TMXReplay, TMXUser, TMIOUser, TMIOReplay

from datetime import datetime

G_TOP_LENGTH = 30


class ControllerUpdater:
    def __init__(self, repoFactory: RepositoryFactory, api: ApiAdaptor):
        self._repoFactory = repoFactory
        self._api = api

    def update_db_maps(self, repoFactory: RepositoryFactory, playerid: int):
        repoMap = repoFactory.getTmxMapRepo()

        all_maps = list()
        curr_page = 1
        maps = self._api.search_maps(playerid, 100, curr_page)
        all_maps += maps["results"]
        totalItemCount = maps["totalItemCount"]
        while totalItemCount < len(all_maps):
            logging.info(f"Downloading maps {len(all_maps)} / {totalItemCount}")
            prevAllMapsCount = len(all_maps)
            curr_page += 1
            maps = self._api.search_maps(playerid, 100, curr_page)
            all_maps += maps["results"]
            if len(all_maps) == prevAllMapsCount:
                break
        for m in all_maps:
            new_map = TMXMap(
                    trackID=m["TrackID"],
                    trackUID=m["TrackUID"],
                    trackName=m["Name"],
                    authorLogin=m["AuthorLogin"],
                    authorTime=int(m["AuthorTime"]),
                    lastUpdatedOfflineRecords=0,
                    lastUpdatedOnlineRecords=0)
            if not repoMap.get(new_map.trackID):
                logging.info(f"New map: {new_map}")
                repoMap.save(new_map)

    def update_db_offline_replays(self,
                                  repoFactory: RepositoryFactory,
                                  track: TMXMap):
        repoMaps = repoFactory.getTmxMapRepo()
        repoReplays = repoFactory.getTmxReplayRepo()
        repoUsers = repoFactory.getTmxUserRepo()

        logging.info(f"Getting offline records for {track.trackName}")
        all_replays = self._api.get_offline_records(track.trackID)

        track.lastUpdatedOfflineRecords = int(datetime.now().timestamp())
        repoMaps.save(track)

        logging.info(f"{len(all_replays)} replays available.")
        for replay in all_replays:
            tmx_user = repoUsers.get(replay["UserID"])
            if not tmx_user:
                tmx_user = TMXUser(
                    userID=replay["UserID"],
                    username=replay["Username"]
                )
                logging.info(f"New TMX user: {tmx_user}")
                repoUsers.save(tmx_user)

            tmx_replay = repoReplays.get(replay["ReplayID"])
            if not tmx_replay:
                new_replay = TMXReplay(
                    replayID=replay["ReplayID"],
                    trackID=track.trackID,
                    tmxUserID=tmx_user.userID,
                    uploadTime=int(
                        datetime.strptime(
                            replay["UploadedAt"],
                            "%Y-%m-%dT%H:%M:%S.%f"
                        ).timestamp()
                    ),
                    replayTime=replay["ReplayTime"]
                    )

                logging.info(f"New TMX replay: {new_replay}")
                repoReplays.save(new_replay)

    def update_db_online_replays(self,
                                 repoFactory: RepositoryFactory,
                                 track: TMXMap):
        repoMaps = repoFactory.getTmxMapRepo()
        repoUsers = repoFactory.getTmioUserRepo()
        repoReplays = repoFactory.getTmioReplayRepo()

        logging.info(f"Getting online records for {track.trackName}")
        all_replays = self._api.get_online_records(track.trackUID,
                                                   0,
                                                   G_TOP_LENGTH)

        track.lastUpdatedOnlineRecords = int(datetime.now().timestamp())
        repoMaps.save(track)

        replays = all_replays['tops']
        nReplays = len(replays) if replays else 0

        logging.info(f"{nReplays} replays available.")
        if nReplays == 0:
            return

        for replay in replays:
            tmio_user = repoUsers.get(replay["player"]["id"])
            if not tmio_user:
                tmio_user = TMIOUser(
                        userID=replay["player"]["id"],
                        name=replay["player"]["name"]
                )
                logging.info(f"New TMIO user: {tmio_user}")
                repoUsers.save(tmio_user)

            tmio_replay = repoReplays.get(replay["url"])
            if not tmio_replay:
                new_replay = TMIOReplay(
                        playerID=tmio_user.userID,
                        time=replay["time"],
                        position=replay["position"],
                        uploadTime=int(
                            datetime.strptime(
                                replay["timestamp"],
                                "%Y-%m-%dT%H:%M:%S%z"
                            ).timestamp()
                        ),
                        url=replay["url"],
                        trackID=track.trackID
                )
                logging.info(f"New TMIO replay: {new_replay}")
                repoReplays.save(new_replay)

    def update_oldest_records(self, repoFactory: RepositoryFactory):
        repoMap = repoFactory.getTmxMapRepo()

        all_tracks = repoMap.findAll()
        if len(all_tracks) == 0:
            return False

        # This logic should probably be on the repository, but it's fine.
        all_tracks.sort(key=lambda t: t.lastUpdate())

        oldest_track = all_tracks[0]
        off_dt = datetime.fromtimestamp(oldest_track.lastUpdatedOfflineRecords)
        on_dt = datetime.fromtimestamp(oldest_track.lastUpdatedOnlineRecords)
        logging.info(f"Next updated track is: {oldest_track.trackName}")
        logging.info(f"Last offline replays update on: {off_dt}")
        logging.info(f"Last online replays update on: {on_dt}")

        min_update_interval = 60 * 60 * 24
        curr_time = datetime.now().timestamp()
        oldest_dt = oldest_track.lastUpdate()

        if oldest_dt > curr_time - min_update_interval:
            next_dt = datetime.fromtimestamp(oldest_dt + min_update_interval)
            logging.info(f"Skipping update. Next update on {next_dt}")
            return False

        if oldest_track.lastUpdatedOfflineRecords < \
                oldest_track.lastUpdatedOnlineRecords:
            self.update_db_offline_replays(repoFactory, oldest_track)
        else:
            self.update_db_online_replays(repoFactory, oldest_track)

        return True


if __name__ == "__main__":
    pass
