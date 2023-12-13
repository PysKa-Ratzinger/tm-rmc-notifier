#!/usr/bin/env python3

from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from datetime import datetime

from models import Base
from models import TMXMap, TMXReplay, TMXUser, TMIOUser, TMIOReplay, APIMeta


class TMXMapRepository:
    def __init__(self, session: Session):
        self._session: Session = session

    def findAll(self) -> list[TMXMap]:
        stmt = select(TMXMap)
        return self._session.scalars(stmt).all()

    def get(self, trackID: int) -> TMXMap:
        stmt = select(TMXMap).where(TMXMap.trackID == trackID)
        try:
            return self._session.scalars(stmt).one()
        except NoResultFound:
            return None

    def save(self, track: TMXMap):
        self._session.add(track)


class TMXReplayRepository:
    def __init__(self, session: Session):
        self._session = session

    def get(self, replayID: int) -> TMXReplay:
        stmt = select(TMXReplay).where(TMXReplay.replayID == replayID)
        try:
            return self._session.scalars(stmt).one()
        except NoResultFound:
            return None

    def save(self, replay: TMXReplay):
        self._session.add(replay)

    def getReplaysSince(self, uploadTime) -> list[TMXReplay]:
        stmt = select(TMXReplay).where(TMXReplay.uploadTime >= uploadTime)
        return self._session.scalars(stmt)


class TMXUserRepository:
    def __init__(self, session: Session):
        self._session = session

    def findAll(self) -> list[TMXUser]:
        stmt = select(TMXUser)
        return self._session.scalars(stmt).all()

    def get(self, userID: int) -> TMXUser:
        stmt = select(TMXUser).where(TMXUser.userID == userID)
        try:
            return self._session.scalars(stmt).one()
        except NoResultFound:
            return None

    def save(self, user: TMXUser):
        self._session.add(user)


class TMIOReplayRepository:
    def __init__(self, session: Session):
        self._session = session

    def get(self, url: str) -> TMIOReplay:
        stmt = select(TMIOReplay).where(TMIOReplay.url == url)
        try:
            return self._session.scalars(stmt).one()
        except NoResultFound:
            return None

    def save(self, replay: TMIOReplay):
        self._session.add(replay)

    def getReplaysSince(self, uploadTime) -> list[TMIOReplay]:
        stmt = select(TMIOReplay).where(TMIOReplay.uploadTime >= uploadTime)
        return self._session.scalars(stmt)


class TMIOUserRepository:
    def __init__(self, session: Session):
        self._session = session

    def findAll(self) -> list[TMIOUser]:
        stmt = select(TMIOUser)
        return self._session.scalars(stmt).all()

    def get(self, userID: int) -> TMIOUser:
        stmt = select(TMIOUser).where(TMIOUser.userID == userID)
        try:
            return self._session.scalars(stmt).one()
        except NoResultFound:
            return None

    def save(self, user: TMIOUser):
        self._session.add(user)


class APIMetaRepository:
    def __init__(self, session: Session):
        self._session = session

    def getMeta(self) -> APIMeta:
        stmt = select(APIMeta)
        try:
            return self._session.scalars(stmt).one()
        except NoResultFound:
            meta = APIMeta()
            meta.lastRequestTimestamp = 0
            self._session.add(meta)
            return self._session.scalars(stmt).one()

    def save(self):
        self._session.commit()


class RepositoryFactory:
    def __init__(self):
        self._db_engine = create_engine("sqlite:///./db.db", echo=False)
        Base.metadata.create_all(self._db_engine)
        self._session = Session(self._db_engine)

    def __del__(self):
        self._session.commit()

    def getTmxMapRepo(self):
        return TMXMapRepository(self._session)

    def getTmxReplayRepo(self):
        return TMXReplayRepository(self._session)

    def getTmxUserRepo(self):
        return TMXUserRepository(self._session)

    def getTmioReplayRepo(self):
        return TMIOReplayRepository(self._session)

    def getTmioUserRepo(self):
        return TMIOUserRepository(self._session)

    def getAPIMetaRepo(self):
        return APIMetaRepository(self._session)


if __name__ == "__main__":
    pass
