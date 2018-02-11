"""Handle data manipulation."""

import json
import os.path

from miscoined import app


def load_file(config_name):
    with open(app.config[config_name]) as fp:
        return json.load(fp)


def put_file(directory, filename, data):
    with open(os.path.join(app.config[directory], filename), "w") as fp:
        return json.dump(data, fp, indent=2)


def occupations():
    occupations = load_file("OCCUPATIONS_FILE")
    for occupation in occupations:
        options = occupation["abilities"]["options"]
        categories = options["categories"]
        del options["categories"]

        if categories is None:
            options["allowed"] = [ability["name"] for
                                  ability in all_abilities()]
            continue

        for category in categories:
            options["allowed"].extend([
                ability["name"] for ability in all_abilities()
                if category in ability["category"]
            ])
    return occupations


def all_abilities():
    return general_abilities() + investigative_abilities()


def general_abilities():
    abilities = load_file("GENERAL_ABILITIES_FILE")
    for ability in abilities:
        ability["category"] = ["general"]
    return abilities


def investigative_abilities():
    abilities = load_file("INVESTIGATIVE_ABILITIES_FILE")
    for ability in abilities:
        ability["category"] = ["investigative", ability["category"]]
    return abilities


def blank_character():
    return load_file("BLANK_CHARACTER_FILE")
