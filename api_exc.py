#!/usr/bin/env python3


class RateLimitException(Exception):
    def __init__(self, msg, waiting_time):
        super().__init__(msg)
        self._wtime = waiting_time

    def get_waiting_time(self):
        return self._wtime


if __name__ == "__main__":
    pass
