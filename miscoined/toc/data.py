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
                                  ability in abilities()]
            continue

        for category in categories:
            options["allowed"].extend([
                ability["name"] for ability in abilities()
                if category in ability["category"]
            ])
    return occupations


def abilities():
    abilities = load_file("GENERAL_ABILITIES_FILE")
    for ability in abilities:
        ability["category"] = ["general"]
    for ability in load_file("INVESTIGATIVE_ABILITIES_FILE"):
        ability["category"] = ["investigative", ability["category"]]
        abilities.append(ability)
    for ability in abilities:
        ability["value"] = 0
        ability["temp"] = 0
    return abilities
