#!/usr/bin/env python3

import os
import json


class Config:
    def __init__(self):
        default_conf = {
            "updated_time": 0,
            "last_updated_time": 0,
        }

        if not os.path.exists("./config"):
            conf = default_conf

        else:
            with open("./config", "rb") as fc:
                try:
                    conf = json.loads(fc.read())
                except Exception:
                    conf = default_conf

        self.updated_time = conf["updated_time"]
        self.last_updated_time = conf["last_updated_time"]

    def save(self):
        with open("./config", "wb") as fc:
            fc.write(json.dumps({
                "updated_time": self.updated_time,
                "last_updated_time": self.last_updated_time
            }).encode())


if __name__ == "__main__":
    pass
