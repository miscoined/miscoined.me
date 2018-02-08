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
    return load_file("OCCUPATIONS_FILE")


def general_abilities():
    return load_file("GENERAL_ABILITIES_FILE")


def investigative_abilities():
    return load_file("INVESTIGATIVE_ABILITIES_FILE")


def blank_character():
    return load_file("BLANK_CHARACTER_FILE")
