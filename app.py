import random
from decimal import Decimal
from uuid import uuid4
import json

from flask import Flask

app = Flask(__name__)

API_VERSION_V1 = 'v1'


class RandomNumberGenerator:

    def __init__(self, chance, total_numbers, winner_numbers_list, winner_number, won):
        self.uuid = str(uuid4())
        self.chance = chance
        self.chance_readable = str(chance) + "%"
        self.total_numbers = total_numbers
        self.winner_numbers_list = winner_numbers_list
        self.winner_number = winner_number
        self.won = won

    def to_json(self):
        return json.dumps(self.__dict__)


@app.route("/" + API_VERSION_V1 + "/random/percentage/")
def error():
    return '{"error": "Chance is empty. Usage: /random/percentage/50.5"}'


@app.route("/" + API_VERSION_V1 + "/random/percentage/<chance>")
def index(chance: str):

    if chance is None or chance == "":
        return '{"error": "Chance is empty. Usage: /random/percentage/50.5"}'

    c = round(float(chance), 2)
    app.logger.debug("Chance = " + str(round(float(chance), 2)) + "%")
    is_whole = c % 1 == 0
    app.logger.debug("Is whole: " + str(c % 1 == 0))
    exponent_number = get_exponential_number(c, is_whole)
    app.logger.debug("Number of exponents: " + str(exponent_number))
    number_list = [*range(1, get_list_number_multiplier(exponent_number, is_whole) + 1, 1)]
    app.logger.debug("Number list size: " + str(len(number_list)))
    random.seed()
    winner_numbers = random.sample(number_list, get_amount_of_winner_numbers(c, is_whole))
    app.logger.debug("winner list size: " + str(len(winner_numbers)))
    winner_number = random.choice(number_list)
    app.logger.debug("Winner number: " + str(winner_number))
    won = winner_number in winner_numbers

    return RandomNumberGenerator(c, len(number_list), winner_numbers, winner_number, won).to_json()


def get_exponential_number(chance: float, is_whole: bool):
    if is_whole:
        return 0
    return abs(Decimal(chance).as_tuple().exponent)


def get_list_number_multiplier(exponent_number: int, is_whole: bool):
    if is_whole:
        return 100
    return 100 * pow(10, exponent_number)


def get_amount_of_winner_numbers(chance: float, is_whole: bool):
    if is_whole:
        return int(chance)
    return int(chance * pow(10, get_exponential_number(chance, is_whole)))
