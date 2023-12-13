#!/usr/bin/env python3

import json
from api_strategy import ApiStrategy


class ApiMockupStrategy(ApiStrategy):
    def __init__(self):
        pass

    def search_maps(self, authorid, limit, page):
        return json.loads("""{
               "results":[
                  {
                     "TrackID":19387,
                     "UserID":27144,
                     "Username":"htimh1",
                     "GbxMapName":"MIDNIGHT METROPOLIS",
                     "AuthorLogin":"FE_OBpuQSvmlsJFIvMBWbw",
                     "MapType":"TM_Race",
                     "TitlePack":"Trackmania",
                     "TrackUID":"QleO8OiNAkIXrZs6r0YLSrLBjEi",
                     "Mood":"48x48Night",
                     "DisplayCost":33603,
                     "ModName":"",
                     "Lightmap":8,
                     "ExeVersion":"3.3.0",
                     "ExeBuild":"2020-10-09_10_58",
                     "AuthorTime":55910,
                     "ParserVersion":1,
                     "UploadedAt":"2020-10-28T18:44:42.18",
                     "UpdatedAt":"2020-10-28T18:44:42.18",
                     "Name":"MIDNIGHT METROPOLIS",
                     "Tags":"3,7,22",
                     "TypeName":"Script",
                     "StyleName":"Scenery",
                     "EnvironmentName":"Stadium",
                     "VehicleName":"CarSport",
                     "UnlimiterRequired":false,
                     "RouteName":"Single",
                     "LengthName":"1 min",
                     "DifficultyName":"Intermediate",
                     "Laps":1,
                     "ReplayWRID":17673,
                     "ReplayWRTime":54193,
                     "ReplayWRUserID":22215,
                     "ReplayWRUsername":"Insanity",
                     "TrackValue":605,
                     "Comments":"...",
                     "MappackID":0,
                     "Unlisted":false,
                     "Unreleased":false,
                     "Downloadable":true,
                     "RatingVoteCount":0,
                     "RatingVoteAverage":0.0,
                     "HasScreenshot":true,
                     "HasThumbnail":true,
                     "HasGhostBlocks":false,
                     "EmbeddedObjectsCount":181,
                     "EmbeddedItemsSize":1493546,
                     "IsMP4":true,
                     "SizeWarning":false,
                     "AwardCount":236,
                     "CommentCount":53,
                     "ReplayCount":36,
                     "ImageCount":4,
                     "VideoCount":1
                  }
               ],
               "totalItemCount":27536
            }""")

    def get_offline_records(self, trackid):
        return json.loads("""[
           {
              "ReplayID":28422,
              "UserID":19595,
              "Username":"Febi",
              "TrackID":19387,
              "UploadedAt":"2021-02-26T12:09:25.477",
              "ReplayTime":78373,
              "StuntScore":0,
              "Respawns":-1,
              "Position":1,
              "Beaten":4,
              "Percentage":100,
              "ReplayPoints":26.0,
              "NadeoPoints":0,
              "ExeBuild":"2020-07-07_23_07",
              "PlayerModel":"CarSport"
           }
        ]""")

    def get_online_records(self, trackuid, offset, length):
        return json.loads("""{
              "tops": [
                {
                  "player": {
                    "name": "aaaaaaGeTFr0z3n",
                    "tag": "SNOW",
                    "id": "4bc3ceea-41ab-426f-b940-f15d00529128",
                    "zone": {
                      "name": "Ontario",
                      "flag": "Ontario",
                      "parent": {
                        "name": "Canada",
                        "flag": "CAN",
                        "parent": {
                          "name": "North America",
                          "flag": "namerica",
                          "parent": {
                            "name": "World",
                            "flag": "WOR"
                          }
                        }
                      }
                    },
                    "meta": {}
                  },
                  "position": 1,
                  "time": 7410,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_4bc3ceea-41ab-426f-b940-f15d00529128_(0'7''41).replay.gbx",
                  "timestamp": "2023-11-26T06:34:06+00:00",
                  "url": "/api/download/ghost/ab1971b7-1fbe-451a-bc1c-15e694e35d8d"
                },
                {
                  "player": {
                    "name": "Pnisj",
                    "id": "f8dd65d6-dbb7-4e99-b493-9d7d6878775f",
                    "zone": {
                      "name": "Norway",
                      "flag": "NOR",
                      "parent": {
                        "name": "Europe",
                        "flag": "europe",
                        "parent": {
                          "name": "World",
                          "flag": "WOR"
                        }
                      }
                    },
                    "meta": {}
                  },
                  "position": 2,
                  "time": 7586,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_f8dd65d6-dbb7-4e99-b493-9d7d6878775f_(0'7''58).replay.gbx",
                  "timestamp": "2023-11-26T05:59:04+00:00",
                  "url": "/api/download/ghost/f3262ff7-5024-4cc6-944b-cfd10f5d485b"
                },
                {
                  "player": {
                    "name": "Cactus_King",
                    "id": "958984be-493b-475d-8b87-5f7b8c1a4006",
                    "zone": {
                      "name": "Noord-Brabant",
                      "flag": "Noord-Brabant",
                      "parent": {
                        "name": "Netherlands",
                        "flag": "NED",
                        "parent": {
                          "name": "Europe",
                          "flag": "europe",
                          "parent": {
                            "name": "World",
                            "flag": "WOR"
                          }
                        }
                      }
                    },
                    "meta": {}
                  },
                  "position": 3,
                  "time": 7960,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_958984be-493b-475d-8b87-5f7b8c1a4006_(0'7''96).replay.gbx",
                  "timestamp": "2023-12-06T17:42:09+00:00",
                  "url": "/api/download/ghost/6ed33557-0d0d-4111-b477-9e27a32741b0"
                },
                {
                  "player": {
                    "name": "UnprovenRuben",
                    "tag": "$F00(!)",
                    "id": "7df4f91e-e3b4-407b-9fe0-ad854ca147b6",
                    "zone": {
                      "name": "Madeira",
                      "flag": "Madeira",
                      "parent": {
                        "name": "Portugal",
                        "flag": "POR",
                        "parent": {
                          "name": "Europe",
                          "flag": "europe",
                          "parent": {
                            "name": "World",
                            "flag": "WOR"
                          }
                        }
                      }
                    }
                  },
                  "position": 4,
                  "time": 8120,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_7df4f91e-e3b4-407b-9fe0-ad854ca147b6_(0'8''12).replay.gbx",
                  "timestamp": "2023-11-26T18:44:57+00:00",
                  "url": "/api/download/ghost/989f440b-87ef-450c-8a1e-93f22ba787bc"
                },
                {
                  "player": {
                    "name": "AzuraFlash",
                    "tag": "❄",
                    "id": "5bc0d921-a0b5-4564-b0b3-fc993a84f14c",
                    "zone": {
                      "name": "Quebec",
                      "flag": "Quebec",
                      "parent": {
                        "name": "Canada",
                        "flag": "CAN",
                        "parent": {
                          "name": "North America",
                          "flag": "namerica",
                          "parent": {
                            "name": "World",
                            "flag": "WOR"
                          }
                        }
                      }
                    }
                  },
                  "position": 5,
                  "time": 8362,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_5bc0d921-a0b5-4564-b0b3-fc993a84f14c_(0'8''36).replay.gbx",
                  "timestamp": "2023-11-27T03:44:56+00:00",
                  "url": "/api/download/ghost/4fc426e4-9210-4b2a-a178-065504f550cd"
                },
                {
                  "player": {
                    "name": "Grootmeister",
                    "tag": "$F22SCUM",
                    "id": "4731e7bd-6c5b-490c-b4e6-df2ff57ae7a3",
                    "zone": {
                      "name": "Norway",
                      "flag": "NOR",
                      "parent": {
                        "name": "Europe",
                        "flag": "europe",
                        "parent": {
                          "name": "World",
                          "flag": "WOR"
                        }
                      }
                    },
                    "meta": {}
                  },
                  "position": 6,
                  "time": 8553,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_4731e7bd-6c5b-490c-b4e6-df2ff57ae7a3_(0'8''55).replay.gbx",
                  "timestamp": "2023-12-03T01:30:24+00:00",
                  "url": "/api/download/ghost/3bb1e6fc-2c7b-4cb1-a6fb-4de81b5f8157"
                },
                {
                  "player": {
                    "name": "riaznad",
                    "id": "26d3b333-fdb7-42fd-9f35-5ced010efbaa",
                    "zone": {
                      "name": "Denmark",
                      "flag": "DEN",
                      "parent": {
                        "name": "Europe",
                        "flag": "europe",
                        "parent": {
                          "name": "World",
                          "flag": "WOR"
                        }
                      }
                    }
                  },
                  "position": 7,
                  "time": 9560,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_26d3b333-fdb7-42fd-9f35-5ced010efbaa_(0'9''56).replay.gbx",
                  "timestamp": "2023-11-30T09:52:11+00:00",
                  "url": "/api/download/ghost/15bf0acf-c724-4ecb-b180-c76b88aa2b19"
                },
                {
                  "player": {
                    "name": "JustUnluckyz",
                    "id": "c401b88e-8eef-4f5d-b6d0-d5400035bbba",
                    "zone": {
                      "name": "Pennsylvania",
                      "flag": "Pennsylvania",
                      "parent": {
                        "name": "United States",
                        "flag": "USA",
                        "parent": {
                          "name": "North America",
                          "flag": "namerica",
                          "parent": {
                            "name": "World",
                            "flag": "WOR"
                          }
                        }
                      }
                    }
                  },
                  "position": 8,
                  "time": 12562,
                  "filename": "Replays\\\\Downloaded\\\\c92b6508-bc6b-4623-a836-c62b395b5221_c401b88e-8eef-4f5d-b6d0-d5400035bbba_(0'12''56).replay.gbx",
                  "timestamp": "2023-12-01T04:26:21+00:00",
                  "url": "/api/download/ghost/082ee056-5e7c-42ee-91fa-d31b4b6c412b"
                }
              ],
              "playercount": 8
            }
        """)


if __name__ == "__main__":
    pass


