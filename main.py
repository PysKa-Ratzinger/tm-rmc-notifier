#!/usr/bin/env python3

import argparse
import time
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

import api_adaptor
from api_exc import RateLimitException
from repositories import RepositoryFactory
from ctrlUpdater import ControllerUpdater
from config import Config


G_MAPPER_PLAYERID = 58100
G_TEST_API = False


def list_users(repoFactory: RepositoryFactory):
    repoTMXUsers = repoFactory.getTmxUserRepo()
    repoTMIOUsers = repoFactory.getTmioUserRepo()

    print("List of all TMX Users")
    for tmx_user in repoTMXUsers.findAll():
        print(f"{tmx_user.userID} - {tmx_user.username}")

    print("List of all TMIO Users")
    for tmio_user in repoTMIOUsers.findAll():
        print(f"{tmio_user.userID} - {tmio_user.name}")


def set_vip_tmio(repoFactory: RepositoryFactory, playerID: str):
    repoTMIOUsers = repoFactory.getTmioUserRepo()

    tmio_user = repoTMIOUsers.get(playerID)
    if not tmio_user:
        print(f"User ({playerID}) not found.")
        return

    if tmio_user.vip:
        print(f"User {tmio_user.name} with ID ({playerID}) was already VIP.")
        return

    tmio_user.vip = True
    print(f"User {tmio_user.name} with ID ({playerID}) is now VIP.")


def set_vip_tmx(repoFactory: RepositoryFactory, playerID: int):
    repoTMXUsers = repoFactory.getTmxUserRepo()

    tmx_user = repoTMXUsers.get(playerID)
    if not tmx_user:
        print(f"User ({playerID}) not found.")
        return

    if tmx_user.vip:
        print(f"User {tmx_user.username} with ID ({playerID}) was " +
              "already VIP.")
        return

    tmx_user.vip = True
    print(f"User {tmx_user.username} with ID ({playerID}) is now VIP.")


def check_vip_replays(repoFactory: RepositoryFactory):
    repoTMXUsers = repoFactory.getTmxUserRepo()
    repoTMIOUsers = repoFactory.getTmioUserRepo()

    print("Offline replays:")
    for tmx_user in repoTMXUsers.findAll():
        if not tmx_user.vip:
            continue
        print(f"Replays driven by: {tmx_user.username}")
        all_replays = list(tmx_user.replays)
        all_replays.sort(key=lambda x: x.uploadTime, reverse=True)
        for tmx_replay in all_replays:
            track = tmx_replay.track
            upload_dt = datetime.fromtimestamp(tmx_replay.uploadTime)
            print(f" - Track: {track.trackName:50s} " +
                  f"UploadTime: {str(upload_dt):30s} " +
                  f"Time: {str(tmx_replay.replayTime):10s}")

    print("Online replays:")
    for tmio_user in repoTMIOUsers.findAll():
        if not tmio_user.vip:
            continue
        print(f"Replays driven by: {tmio_user.name}")
        all_replays = list(tmio_user.replays)
        all_replays.sort(key=lambda x: x.uploadTime, reverse=True)
        for tmio_replay in all_replays:
            track = tmio_replay.track
            upload_dt = datetime.fromtimestamp(tmio_replay.uploadTime)
            print(f" - Track: {track.trackName:50s} " +
                  f"UploadTime: {str(upload_dt):30s} " +
                  f"Time: {str(tmio_replay.time):10s}")


def check_submitted_replays(repoFactory: RepositoryFactory):
    repoTracks = repoFactory.getTmxMapRepo()

    # last_time = conf.last_updated_time

    print("Here is a list of new replays since the last update.")
    all_tracks = repoTracks.findAll()
    print(f"Total maps: {len(all_tracks)}")
    curr_time = datetime.now()
    for track in all_tracks:
        total_replays = len(track.tmx_replays) + len(track.tmio_replays)
        off_dt = datetime.fromtimestamp(track.lastUpdatedOfflineRecords)
        on_dt = datetime.fromtimestamp(track.lastUpdatedOnlineRecords)
        off_delta = (curr_time - off_dt).total_seconds()
        on_delta = (curr_time - on_dt).total_seconds()
        print(f"Track: {track.trackName:50s} ({total_replays}) total " +
              f"replays - {off_delta} / {on_delta}")
        if len(track.tmx_replays) > 0:
            print(f"TMX replays {len(track.tmx_replays)} replays " +
                  f"(last updated {off_delta} ago):")
            for tmx_replay in track.tmx_replays:
                upload_dt = datetime.fromtimestamp(tmx_replay.uploadTime)
                print(f" - UploadTime: {str(upload_dt):30s} " +
                      f"Time: {str(tmx_replay.replayTime):10s} " +
                      f"Driven By: {tmx_replay.tmxUser.username}")
        if len(track.tmio_replays) > 0:
            print(f"TMIO replays {len(track.tmio_replays)} replays " +
                  f"(last updated {on_delta} ago):")
            for tmio_replay in track.tmio_replays:
                upload_dt = datetime.fromtimestamp(tmio_replay.uploadTime)
                print(f" - UploadTime: {str(upload_dt):30s} " +
                      f"Time: {str(tmio_replay.time):10s} " +
                      f"Driven By: {tmio_replay.player.name}")


def update_action(args, conf, repoFactory: RepositoryFactory):
    should_fetch_maps = False

    min_update_interval = 60 * 60
    curr_time = datetime.now().timestamp()
    next_update = conf.updated_time + min_update_interval

    if (args.update_maps or curr_time > next_update):
        should_fetch_maps = True
    else:
        nxt_date = datetime.fromtimestamp(next_update)
        logging.info(f"Skipping map fetching. Next fetch after {nxt_date}.")
        logging.info("Use --update_maps to fetch anyway.")

    api = api_adaptor.get_adaptor(G_TEST_API, repoFactory)
    ctrlUpdater = ControllerUpdater(repoFactory, api)
    should_continue = False

    if should_fetch_maps:
        logging.debug("Updating database.")
        ctrlUpdater.update_db_maps(repoFactory, G_MAPPER_PLAYERID)
        should_continue = True

    else:
        should_continue = ctrlUpdater.update_oldest_records(repoFactory)

    if should_fetch_maps:
        conf.last_updated_time = conf.updated_time
        conf.updated_time = curr_time
        conf.save()

    return should_continue


def do_update(args, conf, repoFactory: RepositoryFactory):
    if not args.continuous:
        try:
            update_action(args, conf, repoFactory)
        except RateLimitException as e:
            logging.error(e)
            sys.exit(1)
    else:
        while True:
            should_wait = False
            wait_time = 0.0

            try:
                if not update_action(args, conf, repoFactory):
                    return
                args.force = False

            except RateLimitException as e:
                should_wait = True
                wait_time = e.get_waiting_time()

            except KeyboardInterrupt:
                break

            if should_wait:
                if args.continuous:
                    if wait_time > 2.0:
                        logging.warning("Rate limited: Waiting " +
                                        f"for {wait_time} seconds")
                    time.sleep(wait_time)
                else:
                    logging.error("Rate limited. Exiting.")


def main(args):
    logFormatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.NOTSET)

    fileHandler = RotatingFileHandler("./log.log",
                                      mode="a",
                                      maxBytes=30*1024*1024,
                                      backupCount=2,
                                      encoding="utf8",
                                      delay=0)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.DEBUG)

    rootLogger.addHandler(fileHandler)
    rootLogger.addHandler(consoleHandler)

    repoFactory = RepositoryFactory()
    conf = Config()

    if args.update:
        do_update(args, conf, repoFactory)

    if args.check_submitted_replays:
        check_submitted_replays(repoFactory)

    if args.check_vip_replays:
        check_vip_replays(repoFactory)

    if args.list_users:
        list_users(repoFactory)

    if args.set_vip_tmx:
        set_vip_tmx(repoFactory, int(args.set_vip_tmx))

    if args.set_vip_tmio:
        set_vip_tmio(repoFactory, args.set_vip_tmio)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--update_maps", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continuous", action="store_true")
    parser.add_argument("--check_submitted_replays", action="store_true")
    parser.add_argument("--check_vip_replays", action="store_true")
    parser.add_argument("--list_users", action="store_true")
    parser.add_argument("--set_vip_tmx")
    parser.add_argument("--set_vip_tmio")
    args = parser.parse_args()

    main(args)
