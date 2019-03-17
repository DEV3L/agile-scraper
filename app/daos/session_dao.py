import pymongo

from app.daos.dao import Dao
from app.daos.mongo import MongoDatabase
from app.models.session import Session


class SpeakerDao(Dao):
    def __init__(self, mongo_database: MongoDatabase):
        super().__init__(mongo_database, 'sessions')

    def find_all(self, *, query: dict = None) -> list:
        results = [result for result in
                   self._mongo_database.find(self.collection, query).sort("session_name", pymongo.ASCENDING)]
        return results

    def _to_json(self, object_record: dict) -> Session:
        session_model = Session()
        session_model.from_json(object_record)
        return session_model
