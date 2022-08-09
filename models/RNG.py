from uuid import uuid4
import json

from sqlalchemy import Column, Integer, String, DateTime, func


def get_rng_from_json(json_rng):
    return json.loads(json_rng, object_hook=lambda d: RandomNumberGenerator(**d))


class RandomNumberGenerator:

    def __init__(self, uuid, chance, total_numbers, winner_numbers_list, winner_number, won):
        self.uuid = uuid
        self.chance = chance
        self.chance_readable = str(chance) + "%"
        self.total_numbers = total_numbers
        self.winner_numbers_list = winner_numbers_list
        self.winner_number = winner_number
        self.won = won

    def to_json(self):
        return json.dumps(self.__dict__)


class RNGS:
    __tablename__ = 'RNGS'

    id = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    uuid = Column(String, primary_key=True, auto_increment=False, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    rng_json = Column(String, nullable=False)

