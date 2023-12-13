#!/usr/bin/env python3

from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class APIMeta(Base):
    __tablename__ = "api_meta"
    id: Mapped[int] = mapped_column(primary_key=True)
    lastRequestTimestamp: Mapped[int]

    def __repr__(self) -> str:
        last_dt = datetime.fromtimestamp(self.lastRequestTimestamp)
        return "APIMeta(" + \
               f"lastRequestTime={last_dt})"


class TMXMap(Base):
    __tablename__ = "tmx_map"
    id: Mapped[int] = mapped_column(primary_key=True)
    trackID: Mapped[int] = mapped_column(unique=True)
    trackUID: Mapped[str]
    trackName: Mapped[str]
    authorLogin: Mapped[str]
    authorTime: Mapped[int]
    lastUpdatedOfflineRecords: Mapped[int]
    lastUpdatedOnlineRecords: Mapped[int]

    tmx_replays: Mapped[List["TMXReplay"]] = relationship(
        back_populates="track", cascade="all, delete-orphan"
    )
    tmio_replays: Mapped[List["TMIOReplay"]] = relationship(
        back_populates="track", cascade="all, delete-orphan"
    )

    def lastUpdate(self):
        return min(self.lastUpdatedOnlineRecords,
                   self.lastUpdatedOfflineRecords)

    def __repr__(self) -> str:
        return "TMXMap(" + \
                f"id={self.id}, " + \
                f"trackID={self.trackID}, " + \
                f"trackUID={self.trackUID}, " + \
                f"trackName={self.trackName}, " + \
                f"authorLogin={self.authorLogin}, " + \
                f"authorTime={self.authorTime}, " + \
                "lastUpdatedOfflineRecords=" + \
                f"{self.lastUpdatedOfflineRecords}, " + \
                f"lastUpdatedOnlineRecords={self.lastUpdatedOnlineRecords})"


class TMXUser(Base):
    __tablename__ = "tmx_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    vip: Mapped[bool]

    replays: Mapped[List["TMXReplay"]] = relationship(
        back_populates="tmxUser", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return "TMXUser(" + \
                f"id={self.id}, " + \
                f"userID={self.userID}, " + \
                f"username={self.username})"


class TMXReplay(Base):
    __tablename__ = "tmx_replay"
    id: Mapped[int] = mapped_column(primary_key=True)
    replayID: Mapped[int]
    trackID: Mapped[int] = mapped_column(ForeignKey("tmx_map.trackID"))
    track: Mapped["TMXMap"] = relationship(back_populates="tmx_replays")
    tmxUserID: Mapped[int] = mapped_column(ForeignKey("tmx_user.userID"))
    tmxUser: Mapped["TMXUser"] = relationship(back_populates="replays")
    uploadTime: Mapped[int]
    replayTime: Mapped[int]

    def __repr__(self) -> str:
        return "TMXReplay(" + \
                f"id={self.id}, " + \
                f"replayID={self.replayID}, " + \
                f"tmxUserID={self.tmxUserID}, " + \
                f"uploadTime={self.uploadTime}, " + \
                f"replayTime={self.replayTime})"


class TMIOUser(Base):
    __tablename__ = "tmio_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    vip: Mapped[bool]

    replays: Mapped[List["TMIOReplay"]] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return "TMIOUser(" + \
                f"id={self.id}, " + \
                f"userID={self.userID}, " + \
                f"name={self.name})"


class TMIOReplay(Base):
    __tablename__ = "tmio_replay"
    id: Mapped[int] = mapped_column(primary_key=True)
    playerID: Mapped[int] = mapped_column(ForeignKey("tmio_user.userID"))
    player: Mapped["TMIOUser"] = relationship(back_populates="replays")
    time: Mapped[int]
    position: Mapped[int]
    uploadTime: Mapped[int]
    url: Mapped[str] = mapped_column(unique=True)
    trackID: Mapped[int] = mapped_column(ForeignKey("tmx_map.trackID"))
    track: Mapped["TMXMap"] = relationship(back_populates="tmio_replays")

    def __repr__(self) -> str:
        return "TMIOReplay(" + \
                f"id={self.id}, " + \
                f"playerID={self.playerID}, " + \
                f"time={self.time}, " + \
                f"position={self.position}, " + \
                f"uploadTime={self.uploadTime}, " + \
                f"url={self.url}, " + \
                f"trackID={self.trackID})"


if __name__ == "__main__":
    pass
