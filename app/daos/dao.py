from app.daos.mongo import MongoDatabase
from app.models.model import Model
from bson import ObjectId


class Dao:
    def __init__(self, mongo_database: MongoDatabase, collection: str):
        self._mongo_database = mongo_database
        self.collection = collection

    # children classes to implement
    def _to_json(self, object_record: dict) -> object:
        raise NotImplemented

    def create(self, model: Model) -> str:
        json = model.to_json()
        object_id = self._mongo_database.create(self.collection, json)
        return object_id

    def find_all(self, *, query: dict = None) -> list:
        results = [result for result in self._mongo_database.find(self.collection, query)]
        return results

    def find_by_id(self, object_id: str) -> object:
        object_record = self._mongo_database.get(self.collection, object_id)
        return self._to_json(object_record)

    def update(self, object_id: str, object_model: Model) -> dict:
        try:
            json = object_model.to_json()
        except AttributeError:
            json = object_model

        return self._mongo_database.mongo_db[self.collection].update_one({'_id': ObjectId(object_id)}, {"$set": json})

    def delete_one(self, object_id: str) -> str:
        return self._mongo_database.mongo_db[self.collection].delete_one({'_id': ObjectId(object_id)})
